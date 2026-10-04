"""
Comprehensive Validator for Codolingo Curriculum Lessons.
Validates JSON schema, structural integrity, item types, deterministic grading, code syntax, and duplicates.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from generator.duplicate_detector import DuplicateDetector
from generator.python_validator import PythonValidator

VALID_TYPES = {
    "micro_lesson",
    "multiple_choice",
    "code_ordering",
    "fill_in_the_blank",
    "code_prediction",
    "fix_the_code",
    "write_the_code",
    "output_prediction",
    "match_code_to_concept",
    "explain_output",
    "error_diagnosis",
    "trace_execution",
    "mini_challenge",
    "guided_project",
    "refactoring_challenge",
    "real_world_scenario",
    "scenario",
}

VALID_DIFFICULTIES = {"easy", "medium", "hard"}

@dataclass
class ValidationResult:
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def summary(self) -> str:
        status = "PASS" if self.valid else "FAIL"
        err_info = f" ({len(self.errors)} errors, {len(self.warnings)} warnings)"
        return f"[{status}]{err_info}"

class CurriculumValidator:
    def __init__(self, python_validator: Optional[PythonValidator] = None, duplicate_detector: Optional[DuplicateDetector] = None):
        self.py_validator = python_validator or PythonValidator()
        self.dup_detector = duplicate_detector or DuplicateDetector()

    def validate_lesson_dict(self, data: Dict[str, Any], execute_code: bool = False) -> ValidationResult:
        """Validate an in-memory lesson dictionary."""
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Top-level keys
        for key in ["lesson_id", "title", "unit", "items"]:
            if key not in data:
                errors.append(f"Missing required top-level key: '{key}'")

        if errors:
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        lesson_id = str(data["lesson_id"])
        items = data.get("items", [])
        item_count = len(items)

        # 2. Item count validation
        if item_count == 0:
            errors.append(f"Lesson {lesson_id} has 0 items")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        if not (25 <= item_count <= 35):
            warnings.append(f"Lesson {lesson_id} item count {item_count} is outside ideal range (28-32, target 30)")

        seen_ids: Set[str] = set()

        # 3. Item-by-item structural and pedagogical checks
        for idx, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"Item at index {idx} is not a valid JSON object")
                continue

            item_id = item.get("id", f"<missing_id_at_{idx}>")
            expected_id = f"{lesson_id}_q{idx}"

            if item_id != expected_id:
                errors.append(f"Item {idx}: Expected ID '{expected_id}', got '{item_id}'")

            if item_id in seen_ids:
                errors.append(f"Duplicate item ID: '{item_id}'")
            seen_ids.add(item_id)

            # Check core required fields
            for field in ["id", "type", "concept", "skill", "difficulty", "prerequisites"]:
                if field not in item:
                    errors.append(f"{item_id}: Missing required field '{field}'")

            itype = item.get("type")
            if itype and itype not in VALID_TYPES:
                errors.append(f"{item_id}: Invalid item type '{itype}'")

            diff = item.get("difficulty")
            if diff and diff not in VALID_DIFFICULTIES:
                errors.append(f"{item_id}: Invalid difficulty '{diff}'")

            prereqs = item.get("prerequisites")
            if prereqs is not None and not isinstance(prereqs, list):
                errors.append(f"{item_id}: 'prerequisites' must be a list")

            # Exercise type-specific validation
            if itype == "micro_lesson":
                if not item.get("title"):
                    errors.append(f"{item_id} (micro_lesson): Missing 'title'")
                if not item.get("content"):
                    errors.append(f"{item_id} (micro_lesson): Missing 'content'")

            elif itype in {"multiple_choice", "code_prediction", "output_prediction", "real_world_scenario", "scenario"}:
                prompt = item.get("prompt", "")
                if not prompt:
                    errors.append(f"{item_id} ({itype}): Missing 'prompt'")
                options = item.get("options")
                if not options or not isinstance(options, list) or len(options) < 2:
                    errors.append(f"{item_id} ({itype}): 'options' must be a list with at least 2 choices")
                correct = item.get("correct_answer")
                if not correct:
                    errors.append(f"{item_id} ({itype}): Missing 'correct_answer'")
                if not item.get("explanation"):
                    warnings.append(f"{item_id} ({itype}): Missing 'explanation'")

            elif itype == "match_code_to_concept":
                prompt = item.get("prompt", "")
                if not prompt:
                    errors.append(f"{item_id} (match_code_to_concept): Missing 'prompt'")
                options = item.get("options")
                correct = item.get("correct_answer")
                if not options:
                    errors.append(f"{item_id} (match_code_to_concept): Missing 'options'")
                if not correct:
                    errors.append(f"{item_id} (match_code_to_concept): Missing 'correct_answer'")
                if not item.get("explanation"):
                    warnings.append(f"{item_id} (match_code_to_concept): Missing 'explanation'")

            elif itype == "code_ordering":
                if not item.get("prompt"):
                    errors.append(f"{item_id} (code_ordering): Missing 'prompt'")
                options = item.get("options")
                correct = item.get("correct_answer")
                if not isinstance(options, list) or not isinstance(correct, list):
                    errors.append(f"{item_id} (code_ordering): 'options' and 'correct_answer' must be lists")
                elif sorted(options) != sorted(correct):
                    errors.append(f"{item_id} (code_ordering): 'options' and 'correct_answer' item sets do not match")

            elif itype == "fill_in_the_blank":
                if not item.get("prompt"):
                    errors.append(f"{item_id} (fill_in_the_blank): Missing 'prompt'")
                if "accepted_answers" not in item and "correct_answer" not in item and "expected_output" not in item:
                    errors.append(f"{item_id} (fill_in_the_blank): Missing 'accepted_answers', 'correct_answer', or 'expected_output'")

            elif itype in {"fix_the_code", "write_the_code", "mini_challenge", "refactoring_challenge", "guided_project"}:
                if not item.get("prompt"):
                    errors.append(f"{item_id} ({itype}): Missing 'prompt'")
                if "starter_code" not in item and "code" not in item:
                    warnings.append(f"{item_id} ({itype}): Missing 'starter_code'")
                if "solution_code" not in item and "correct_answer" not in item:
                    errors.append(f"{item_id} ({itype}): Missing 'solution_code' or 'correct_answer'")

            # 4. Local Python code validation
            code_errs, code_warns = self.py_validator.validate_item_code(item, execute_code=execute_code)
            errors.extend(code_errs)
            warnings.extend(code_warns)

        # 5. Duplicate and repetition detection
        dup_errs, dup_warns = self.dup_detector.check_lesson_items(items)
        errors.extend(dup_errs)
        warnings.extend(dup_warns)

        is_valid = (len(errors) == 0)
        return ValidationResult(valid=is_valid, errors=errors, warnings=warnings)

    def validate_file(self, filepath: Path, execute_code: bool = False) -> ValidationResult:
        """Validate a lesson file on disk."""
        filepath = Path(filepath)
        if not filepath.exists():
            return ValidationResult(valid=False, errors=[f"File not found: {filepath}"])

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return ValidationResult(valid=False, errors=[f"JSON syntax error in {filepath.name}: {e}"])

        return self.validate_lesson_dict(data, execute_code=execute_code)
