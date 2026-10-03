"""
Comprehensive Validator for Codolingo Python Curriculum
Validates structural integrity, pedagogical quality, code validity, and deterministic grading.
"""

import ast
import json
import os
import re
import sys
from pathlib import Path

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

def validate_lesson_file(filepath):
    errors = []
    warnings = []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"JSON Parse Error: {e}"], []

    for key in ["lesson_id", "title", "unit", "items"]:
        if key not in data:
            errors.append(f"Missing top-level key: {key}")

    if errors:
        return errors, warnings

    lesson_id = data["lesson_id"]
    items = data.get("items", [])
    item_count = len(items)

    if not (25 <= item_count <= 35):
        warnings.append(f"Item count {item_count} is outside ideal range (28-32, target 30)")
    if item_count == 0:
        errors.append("Lesson has 0 items")
        return errors, warnings

    seen_ids = set()
    seen_prompts = set()
    item_ids = {it.get("id") for it in items if "id" in it}

    for idx, item in enumerate(items, start=1):
        item_id = item.get("id", f"<missing_id_at_{idx}>")
        expected_id = f"{lesson_id}_q{idx}"
        
        if item_id != expected_id:
            errors.append(f"Item {idx}: Expected ID '{expected_id}', got '{item_id}'")
            
        if item_id in seen_ids:
            errors.append(f"Duplicate item ID: '{item_id}'")
        seen_ids.add(item_id)

        # Check required fields
        for field in ["id", "type", "concept", "skill", "difficulty", "prerequisites"]:
            if field not in item:
                errors.append(f"{item_id}: Missing required field '{field}'")

        itype = item.get("type")
        if itype and itype not in VALID_TYPES:
            errors.append(f"{item_id}: Invalid item type '{itype}'")

        diff = item.get("difficulty")
        if diff and diff not in VALID_DIFFICULTIES:
            errors.append(f"{item_id}: Invalid difficulty '{diff}'")

        # Type-specific validation
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
                errors.append(f"{item_id} ({itype}): 'options' must be a list of at least 2 items")
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
                errors.append(f"{item_id} (code_ordering): 'options' and 'correct_answer' set elements do not match")
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

        # Python Code Syntax Validation
        for code_field in ["starter_code", "solution_code", "code"]:
            code_str = item.get(code_field)
            if code_str and isinstance(code_str, str):
                # Don't fail syntax check on intentional errors or pseudo templates
                is_intentional_err = (
                    itype in {"fix_the_code", "error_diagnosis"} and code_field in {"starter_code", "code"}
                ) or "____" in code_str or "<" in code_str and ">" in code_str
                if not is_intentional_err:
                    try:
                        ast.parse(code_str)
                    except SyntaxError as syn_err:
                        warnings.append(f"{item_id} ({code_field}): SyntaxError: {syn_err}")

        # Check prompt uniqueness
        prompt_text = item.get("prompt") or item.get("title") or ""
        norm_prompt = re.sub(r"\s+", " ", prompt_text.strip().lower())
        if norm_prompt and len(norm_prompt) > 15:
            if norm_prompt in seen_prompts:
                warnings.append(f"{item_id}: Duplicate prompt detected ('{prompt_text[:30]}...')")
            seen_prompts.add(norm_prompt)

    return errors, warnings

def validate_all(root_dir="python_content"):
    root = Path(root_dir)
    if not root.exists():
        print(f"Directory {root_dir} does not exist.")
        return False
        
    all_files = sorted(root.glob("**/*.json"))
    total_files = len(all_files)
    total_errors = 0
    total_warnings = 0
    
    print(f"=== Codolingo Curriculum Validator ===")
    print(f"Found {total_files} lesson file(s) in {root_dir}\n")
    
    for filepath in all_files:
        errors, warnings = validate_lesson_file(filepath)
        status = "PASS" if not errors else "FAIL"
        warn_str = f" ({len(warnings)} warnings)" if warnings else ""
        print(f"[{status}] {filepath.name}{warn_str}")
        for err in errors:
            print(f"   [ERROR] {err}")
            total_errors += 1
        for warn in warnings:
            print(f"   [WARN]  {warn}")
            total_warnings += 1

    print("\n-------------------------------------------")
    print(f"Validation complete: {total_files} files checked.")
    print(f"Total Errors: {total_errors}, Total Warnings: {total_warnings}")
    return total_errors == 0

if __name__ == "__main__":
    success = validate_all()
    sys.exit(0 if success else 1)
