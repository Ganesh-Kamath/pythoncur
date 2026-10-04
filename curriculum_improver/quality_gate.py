"""
Deterministic Quality Gate for Codolingo Improvement Engine.
Validates code syntax, sandbox execution, MCQ determinism, and schema integrity before any AI review.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from generator.python_validator import PythonValidator
from generator.validator import VALID_TYPES, VALID_DIFFICULTIES

@dataclass
class GateResult:
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class QualityGate:
    def __init__(self, python_validator: Optional[PythonValidator] = None):
        self.py_validator = python_validator or PythonValidator()

    def validate_item(self, item: Dict[str, Any], execute_code: bool = True) -> GateResult:
        """Thoroughly validate a proposed exercise modification deterministically."""
        errors: List[str] = []
        warnings: List[str] = []

        item_id = item.get("id", "unknown_item")

        # 1. Required core fields
        for field_name in ["id", "type", "concept", "skill", "difficulty"]:
            if field_name not in item or not item[field_name]:
                errors.append(f"{item_id}: Missing or empty required field '{field_name}'")

        itype = item.get("type", "")
        if itype not in VALID_TYPES:
            errors.append(f"{item_id}: Unknown exercise type '{itype}'")

        diff = item.get("difficulty", "")
        if diff not in VALID_DIFFICULTIES:
            errors.append(f"{item_id}: Unknown difficulty '{diff}'")

        # 2. Type-specific checks
        if itype == "micro_lesson":
            if not item.get("title"):
                errors.append(f"{item_id} (micro_lesson): Missing 'title'")
            if not item.get("content") or len(str(item.get("content")).strip()) < 30:
                errors.append(f"{item_id} (micro_lesson): 'content' is missing or too brief")

        elif itype in {"multiple_choice", "code_prediction", "output_prediction", "scenario", "real_world_scenario"}:
            prompt = item.get("prompt", "")
            if not prompt:
                errors.append(f"{item_id} ({itype}): Missing 'prompt'")
            opts = item.get("options")
            if not opts or not isinstance(opts, list) or len(opts) < 2:
                errors.append(f"{item_id} ({itype}): 'options' must be a list of at least 2 choices")
            correct = item.get("correct_answer")
            if not correct:
                errors.append(f"{item_id} ({itype}): Missing 'correct_answer'")
            elif isinstance(correct, str) and correct.upper() in {"A", "B", "C", "D"}:
                # Verify that options correspond to the choice letter
                c_upper = correct.upper()
                prefix = f"{c_upper}."
                has_match = any(str(o).strip().startswith(prefix) or str(o).strip() == correct for o in opts)
                if not has_match:
                    errors.append(f"{item_id}: Correct answer '{correct}' has no matching option in {opts}")
            else:
                # Direct string answer must be in options
                if not any(str(o).strip() == str(correct).strip() for o in opts):
                    errors.append(f"{item_id}: Correct answer '{correct}' is not present in options {opts}")

        elif itype == "fill_in_the_blank":
            if not item.get("prompt"):
                errors.append(f"{item_id} (fill_in_the_blank): Missing 'prompt'")
            if not item.get("accepted_answers") and not item.get("expected_output") and not item.get("correct_answer"):
                errors.append(f"{item_id} (fill_in_the_blank): Missing accepted answers")

        elif itype == "code_ordering":
            opts = item.get("options")
            correct = item.get("correct_answer")
            if not isinstance(opts, list) or not isinstance(correct, list):
                errors.append(f"{item_id} (code_ordering): 'options' and 'correct_answer' must be lists")
            elif sorted(opts) != sorted(correct):
                errors.append(f"{item_id} (code_ordering): Elements in 'options' and 'correct_answer' do not match")

        elif itype in {"fix_the_code", "write_the_code", "mini_challenge", "refactoring_challenge"}:
            if not item.get("prompt"):
                errors.append(f"{item_id} ({itype}): Missing 'prompt'")
            if "solution_code" not in item and "correct_answer" not in item:
                errors.append(f"{item_id} ({itype}): Missing 'solution_code'")

        # 3. Python code execution & AST checks
        code_errs, code_warns = self.py_validator.validate_item_code(item, execute_code=execute_code)
        errors.extend(code_errs)
        warnings.extend(code_warns)

        return GateResult(passed=(len(errors) == 0), errors=errors, warnings=warnings)
