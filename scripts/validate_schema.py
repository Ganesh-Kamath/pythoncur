"""
Deterministic Schema Validator for Codolingo Python Curriculum.
Verifies structure, required fields, and item contracts across all 244 lessons.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

WORKSPACE = Path(__file__).resolve().parent.parent
CONTENT_DIR = WORKSPACE / "python_content"

VALID_TYPES = {
    "micro_lesson", "multiple_choice", "code_prediction", "fill_in_the_blank",
    "code_ordering", "fix_the_code", "write_the_code", "output_prediction",
    "match_code_to_concept", "explain_output", "error_diagnosis",
    "trace_execution", "mini_challenge", "guided_project",
    "refactoring_challenge", "real_world_scenario"
}

VALID_DIFFICULTIES = {"easy", "medium", "hard", "expert"}

def validate_schema() -> Dict[str, Any]:
    results = {
        "total_lessons": 0,
        "total_items": 0,
        "schema_errors": 0,
        "missing_objectives": 0,
        "missing_prerequisites": 0,
        "error_details": []
    }

    if not CONTENT_DIR.exists():
        results["schema_errors"] += 1
        results["error_details"].append("python_content directory not found")
        return results

    for unit_dir in sorted(CONTENT_DIR.iterdir()):
        if not unit_dir.is_dir() or not unit_dir.name.startswith("unit_"):
            continue
        for lesson_file in sorted(unit_dir.glob("*.json")):
            results["total_lessons"] += 1
            try:
                with open(lesson_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                results["schema_errors"] += 1
                results["error_details"].append(f"JSON syntax error in {lesson_file.name}: {e}")
                continue

            lid = data.get("lesson_id")
            if not lid:
                results["schema_errors"] += 1
                results["error_details"].append(f"Missing lesson_id in {lesson_file.name}")

            if "learning_objectives" not in data or not isinstance(data["learning_objectives"], list) or len(data["learning_objectives"]) == 0:
                results["missing_objectives"] += 1
                results["error_details"].append(f"Lesson {lid} lacks 'learning_objectives'")

            if "prerequisites" not in data or not isinstance(data["prerequisites"], list):
                results["missing_prerequisites"] += 1
                results["error_details"].append(f"Lesson {lid} lacks 'prerequisites'")

            items = data.get("items", [])
            if len(items) != 30:
                results["schema_errors"] += 1
                results["error_details"].append(f"Lesson {lid} has {len(items)} items, expected 30")

            for idx, item in enumerate(items, 1):
                results["total_items"] += 1
                iid = item.get("id", f"{lid}_q{idx}")
                itype = item.get("type")
                if itype not in VALID_TYPES:
                    results["schema_errors"] += 1
                    results["error_details"].append(f"Item {iid} has invalid type: {itype}")

                diff = item.get("difficulty")
                if diff not in VALID_DIFFICULTIES:
                    results["schema_errors"] += 1
                    results["error_details"].append(f"Item {iid} has invalid difficulty: {diff}")

                for req_key in ["id", "type", "concept", "skill", "difficulty", "prerequisites"]:
                    if req_key not in item:
                        results["schema_errors"] += 1
                        results["error_details"].append(f"Item {iid} missing required field '{req_key}'")

    return results

if __name__ == "__main__":
    res = validate_schema()
    print(f"Validated {res['total_lessons']} lessons, {res['total_items']} items.")
    print(f"Schema errors: {res['schema_errors']}")
    print(f"Missing objectives: {res['missing_objectives']}")
    print(f"Missing prerequisites: {res['missing_prerequisites']}")
    if res["schema_errors"] > 0:
        for err in res["error_details"][:10]:
            print(f" - {err}")
        sys.exit(1)
    print("Schema validation: PASS")
