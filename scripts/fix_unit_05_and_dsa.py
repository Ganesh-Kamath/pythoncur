"""
Fixes for Unit 5.2 else clause items and DSA exact outputs:
- 5.2: Replace synthetic items with high-value else-clause reasoning/coding problems
- 33.1_q8, 33.1_q9, 33.1_q12: Align printed representations
- 39.1_q8: Align printed representations
"""

import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PYTHON_CONTENT = WORKSPACE / "python_content"

def update_item(unit_num: int, filename: str, item_id: str, updater):
    path = PYTHON_CONTENT / f"unit_{unit_num:02d}" / filename
    if not path.exists():
        print(f"Error: {path} not found")
        return False
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    found = False
    for it in data.get("items", []):
        if it.get("id") == item_id:
            updater(it)
            found = True
            break
            
    if found:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Fixed {item_id} in {filename}")
        return True
    else:
        print(f"Warning: {item_id} not found in {filename}")
        return False

def run_fixes():
    # 1. 5.2 else clause items
    else_replacements = {
        "5.2_q7": {
            "type": "code_prediction",
            "prompt": "What does this code output?\n```python\nbalance = -5\nif balance >= 0:\n    print('Positive')\nelse:\n    print('Overdrawn')\n```",
            "options": ["Overdrawn", "Positive", "Positive\nOverdrawn", "Error"],
            "correct_answer": "Overdrawn",
            "explanation": "Since `balance >= 0` evaluates to False (-5 is less than 0), Python executes the `else` block, printing 'Overdrawn'."
        },
        "5.2_q8": {
            "type": "multiple_choice",
            "prompt": "Can an `else` block have its own condition like `else x > 5:` in Python?",
            "options": [
                "No, `else` takes no condition; use `elif x > 5:` if an additional condition is required",
                "Yes, Python allows optional conditions after `else`",
                "Yes, but only if enclosed in parentheses",
                "No, `else` can only be used with loops, never with `if`"
            ],
            "correct_answer": "No, `else` takes no condition; use `elif x > 5:` if an additional condition is required",
            "explanation": "An `else` clause catches all remaining cases and cannot accept a condition. If you need a conditional branch, use `elif`."
        },
        "5.2_q9": {
            "type": "fix_the_code",
            "prompt": "Fix this code so that the `else` keyword aligns properly with the `if` statement:",
            "starter_code": "user_role = 'guest'\nif user_role == 'admin':\n    print('Full Access')\n    else:\n        print('Guest Access')",
            "solution_code": "user_role = 'guest'\nif user_role == 'admin':\n    print('Full Access')\nelse:\n    print('Guest Access')",
            "explanation": "The `else` keyword must be at the same indentation level as its matching `if` statement."
        },
        "5.2_q11": {
            "type": "code_prediction",
            "prompt": "What does this snippet display?\n```python\nis_weekend = False\nif is_weekend:\n    print('Rest')\nelse:\n    print('Work')\nprint('Done')\n```",
            "options": ["Work\nDone", "Rest\nDone", "Work", "Rest"],
            "correct_answer": "Work\nDone",
            "explanation": "Because `is_weekend` is False, the `else` branch prints 'Work'. Then, normal sequential execution prints 'Done'."
        },
        "5.2_q12": {
            "type": "output_prediction",
            "prompt": "What will be printed when this script runs?\n```python\nnum = 14\nif num % 2 == 0:\n    print('Even')\nelse:\n    print('Odd')\n```",
            "options": ["Even", "Odd", "0", "None"],
            "correct_answer": "Even",
            "explanation": "14 % 2 equals 0, satisfying the `if` condition and printing 'Even'."
        }
    }
    for qid, nd in else_replacements.items():
        def make_upd(d):
            def upd(it):
                for k, v in d.items():
                    it[k] = v
            return upd
        update_item(5, "5.2_the_else_statement.json", qid, make_upd(nd))

    # 2. 33.1_q8, 33.1_q9, 33.1_q12
    def fix_33_1_8(it):
        it["options"] = [
            "twenty\nKey 20 exists: True\nKey 40 exists: False",
            "twenty\nKey 20 exists: False\nKey 40 exists: True",
            "missing\nKey 20 exists: True\nKey 40 exists: False",
            "Error"
        ]
        it["correct_answer"] = "twenty\nKey 20 exists: True\nKey 40 exists: False"
    update_item(33, "33.1_hash_tables_concepts.json", "33.1_q8", fix_33_1_8)

    def fix_33_1_9(it):
        it["options"] = [
            "{'x': 1, 'z': 3}\nmissing",
            "{'x': 1, 'y': 2, 'z': 3}\nmissing",
            "{'x': 1, 'z': 3}\n2",
            "{'x': 1, 'z': 3}\ny"
        ]
        it["correct_answer"] = "{'x': 1, 'z': 3}\nmissing"
    update_item(33, "33.1_hash_tables_concepts.json", "33.1_q9", fix_33_1_9)

    def fix_33_1_12(it):
        it["options"] = [
            "zero_again\n[0, 1, 2]\n['zero_again', 'one', 'two']",
            "zero\n[0, 1, 2]\n['zero', 'one', 'two']",
            "zero_again\n[0, 1, 2]\n['zero', 'one', 'two']",
            "Error"
        ]
        it["correct_answer"] = "zero_again\n[0, 1, 2]\n['zero_again', 'one', 'two']"
    update_item(33, "33.1_hash_tables_concepts.json", "33.1_q12", fix_33_1_12)

    # 3. 39.1_q8
    def fix_39_1_8(it):
        it["options"] = [
            "found\n['X']",
            "found\n[]",
            "not found\n['X']",
            "Error"
        ]
        it["correct_answer"] = "found\n['X']"
    update_item(39, "39.1_graph_representation.json", "39.1_q8", fix_39_1_8)

if __name__ == "__main__":
    run_fixes()
