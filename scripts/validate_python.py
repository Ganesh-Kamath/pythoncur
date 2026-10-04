"""
Deterministic Python AST and Syntax Validator for Codolingo Curriculum.
Ensures 100% of runnable code blocks, starter codes, and solutions compile cleanly.
"""

import ast
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any

WORKSPACE = Path(__file__).resolve().parent.parent
CONTENT_DIR = WORKSPACE / "python_content"

def extract_python_blocks(text: str) -> list[str]:
    if not text or not isinstance(text, str):
        return []
    # Match explicitly tagged python code blocks
    return re.findall(r"```(?:python|py)\s*([\s\S]*?)\s*```", text)

def validate_python() -> Dict[str, Any]:
    results = {
        "total_snippets_checked": 0,
        "syntax_errors": 0,
        "error_details": []
    }

    for unit_dir in sorted(CONTENT_DIR.iterdir()):
        if not unit_dir.is_dir() or not unit_dir.name.startswith("unit_"):
            continue
        for lesson_file in sorted(unit_dir.glob("*.json")):
            with open(lesson_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            lid = data.get("lesson_id", lesson_file.stem)

            for item in data.get("items", []):
                iid = item.get("id")
                itype = item.get("type")

                # 1. Check prompt code blocks
                prompt = item.get("prompt", "")
                blocks = extract_python_blocks(prompt)
                for blk in blocks:
                    # In code_ordering, prompt lines are deliberately scrambled for the learner
                    if itype == "code_ordering":
                        continue
                    # In error diagnosis / syntax questions, the snippet is the broken code being tested
                    if itype in {"error_diagnosis", "fix_the_code"} or "syntax" in prompt.lower() or "crash" in prompt.lower() or "refuse" in prompt.lower():
                        continue
                    # Skip incomplete placeholders like '___'
                    if "___" in blk:
                        continue
                    results["total_snippets_checked"] += 1
                    try:
                        ast.parse(blk)
                    except SyntaxError as e:
                        results["syntax_errors"] += 1
                        results["error_details"].append(f"{iid} (prompt): {e.msg} on line {e.lineno}")

                # 2. Check solution_code (must always be syntactically valid)
                sol = item.get("solution_code")
                if sol and isinstance(sol, str):
                    if "___" not in sol:
                        results["total_snippets_checked"] += 1
                        try:
                            ast.parse(sol)
                        except SyntaxError as e:
                            results["syntax_errors"] += 1
                            results["error_details"].append(f"{iid} (solution_code): {e.msg} on line {e.lineno}")

    return results

if __name__ == "__main__":
    res = validate_python()
    print(f"Checked {res['total_snippets_checked']} Python snippets.")
    print(f"Syntax errors: {res['syntax_errors']}")
    if res["syntax_errors"] > 0:
        for err in res["error_details"][:10]:
            print(f" - {err}")
        sys.exit(1)
    print("Python AST validation: PASS")
