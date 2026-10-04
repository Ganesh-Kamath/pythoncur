"""
Deterministic Answer and Explanation Consistency Validator for Codolingo Curriculum.
Ensures correct_answer, options, solution_code, and explanations are complete and aligned.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

WORKSPACE = Path(__file__).resolve().parent.parent
CONTENT_DIR = WORKSPACE / "python_content"

def validate_answers() -> Dict[str, Any]:
    results = {
        "total_items_checked": 0,
        "answer_mismatches": 0,
        "missing_answers": 0,
        "missing_solutions": 0,
        "missing_explanations": 0,
        "error_details": []
    }

    for unit_dir in sorted(CONTENT_DIR.iterdir()):
        if not unit_dir.is_dir() or not unit_dir.name.startswith("unit_"):
            continue
        for lesson_file in sorted(unit_dir.glob("*.json")):
            with open(lesson_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            lid = data.get("lesson_id")

            for item in data.get("items", []):
                results["total_items_checked"] += 1
                iid = item.get("id")
                itype = item.get("type")

                # Explanations check
                if itype != "micro_lesson":
                    expl = item.get("explanation", "").strip()
                    if not expl or len(expl.split()) < 4:
                        results["missing_explanations"] += 1
                        results["error_details"].append(f"{iid}: Missing or empty explanation")

                # MCQ / Options matching check
                if itype in {"multiple_choice", "code_prediction", "output_prediction"}:
                    opts = item.get("options")
                    corr = item.get("correct_answer")
                    if not corr:
                        results["missing_answers"] += 1
                        results["error_details"].append(f"{iid}: Missing correct_answer")
                    elif not opts or not isinstance(opts, list) or len(opts) < 2:
                        results["answer_mismatches"] += 1
                        results["error_details"].append(f"{iid}: Less than 2 options")
                    else:
                        corr_str = str(corr).strip()
                        matched = False
                        if corr_str in [str(o).strip() for o in opts]:
                            matched = True
                        elif corr_str.upper() in ["A", "B", "C", "D"]:
                            letter_idx = {"A": 0, "B": 1, "C": 2, "D": 3}[corr_str.upper()]
                            if letter_idx < len(opts):
                                matched = True
                        if not matched:
                            results["answer_mismatches"] += 1
                            results["error_details"].append(f"{iid}: Answer '{corr}' not in options")

                # Code ordering check
                elif itype == "code_ordering":
                    opts = item.get("options")
                    corr = item.get("correct_answer")
                    if not isinstance(opts, list) or not isinstance(corr, list):
                        results["answer_mismatches"] += 1
                        results["error_details"].append(f"{iid}: Options/answer must be lists")
                    elif sorted([str(s).strip() for s in opts]) != sorted([str(s).strip() for s in corr]):
                        results["answer_mismatches"] += 1
                        results["error_details"].append(f"{iid}: Options and answer sets differ")

                # Coding / Debugging solutions check
                elif itype in {"write_the_code", "fix_the_code"}:
                    sol = item.get("solution_code", "").strip()
                    if not sol:
                        results["missing_solutions"] += 1
                        results["error_details"].append(f"{iid}: Missing solution_code")

    return results

if __name__ == "__main__":
    res = validate_answers()
    print(f"Checked {res['total_items_checked']} items.")
    print(f"Answer mismatches: {res['answer_mismatches']}")
    print(f"Missing answers: {res['missing_answers']}")
    print(f"Missing solutions: {res['missing_solutions']}")
    print(f"Missing explanations: {res['missing_explanations']}")
    if res["answer_mismatches"] > 0 or res["missing_solutions"] > 0 or res["missing_explanations"] > 0:
        for err in res["error_details"][:10]:
            print(f" - {err}")
        sys.exit(1)
    print("Answer & explanation validation: PASS")
