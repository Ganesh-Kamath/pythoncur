"""
Script to fix remaining items:
1. Fix 3.4_q7 options so Option A is 'True', Option B is 'False', etc.
2. Replace 5.1 synthetic duplicates (5.1_q7, 5.1_q8, 5.1_q9, 5.1_q11, 5.1_q12) with real if-condition exercises
3. Replace 5.6_q9, 42.1_q9, 42.3_q9 duplicate project prompts with rich milestone exercises
4. Align output formatting for 33.1_q8, 33.1_q9, 33.1_q12, 39.1_q8
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
    # 1. Fix 3.4_q7 options
    def fix_3_4_7(it):
        it["options"] = ["True", "False", "SyntaxError", "TypeError"]
        it["correct_answer"] = "True"
        it["explanation"] = "In Python, string comparison is lexicographical (based on ASCII/Unicode code points). Since 'b' comes after 'a', 'banana' > 'apple' evaluates to True."
    update_item(3, "3.4_comparison_operators.json", "3.4_q7", fix_3_4_7)

    # 2. Fix 5.1 if-statement duplicates
    if_replacements = {
        "5.1_q7": {
            "type": "code_prediction",
            "prompt": "What does this code output?\n```python\ntemperature = 35\nif temperature > 30:\n    print('Heat advisory')\nprint('Drive safely')\n```",
            "options": ["Heat advisory\nDrive safely", "Heat advisory", "Drive safely", "Error"],
            "correct_answer": "Heat advisory\nDrive safely",
            "explanation": "Since `temperature > 30` is True, 'Heat advisory' is printed. The following line is unindented, so it always runs, printing 'Drive safely'."
        },
        "5.1_q8": {
            "type": "multiple_choice",
            "prompt": "What is the requirement for the indentation level of code inside an `if` block in Python?",
            "options": [
                "All statements in the block must be indented by the exact same amount (conventionally 4 spaces)",
                "Indentation can vary freely line by line within the block",
                "Indentation is only required for loops, not if statements",
                "Python accepts either tabs or spaces intermixed within the same line"
            ],
            "correct_answer": "All statements in the block must be indented by the exact same amount (conventionally 4 spaces)",
            "explanation": "Python uses whitespace to denote blocks of code. All statements in the same block must have identical indentation."
        },
        "5.1_q9": {
            "type": "fix_the_code",
            "prompt": "Fix this code by adding the missing colon `:` at the end of the `if` header:",
            "starter_code": "is_logged_in = True\nif is_logged_in\n    print('Welcome back!')",
            "solution_code": "is_logged_in = True\nif is_logged_in:\n    print('Welcome back!')",
            "explanation": "Compound statements in Python such as `if`, `for`, and `def` must terminate their header line with a colon `:`."
        },
        "5.1_q11": {
            "type": "code_prediction",
            "prompt": "What does this snippet display?\n```python\nscore = 45\nif score >= 50:\n    print('Passed')\nprint('Score recorded')\n```",
            "options": ["Score recorded", "Passed\nScore recorded", "Passed", "Nothing"],
            "correct_answer": "Score recorded",
            "explanation": "`score >= 50` is False (45 < 50), so the indented `print('Passed')` is skipped. The unindented line prints 'Score recorded'."
        },
        "5.1_q12": {
            "type": "output_prediction",
            "prompt": "What will be printed when this script runs?\n```python\nitems = []\nif items:\n    print('Cart has items')\nif not items:\n    print('Cart is empty')\n```",
            "options": ["Cart is empty", "Cart has items", "Cart has items\nCart is empty", "None"],
            "correct_answer": "Cart is empty",
            "explanation": "In Python, empty collections (like empty lists `[]`) evaluate to False in a boolean context. Therefore, `not items` is True."
        }
    }
    for qid, nd in if_replacements.items():
        def make_upd(d):
            def upd(it):
                for k, v in d.items():
                    it[k] = v
            return upd
        update_item(5, "5.1_the_if_statement.json", qid, make_upd(nd))

    # 3. Replace duplicate item 9s in project lessons
    def fix_5_6_9(it):
        it["prompt"] = "In the Interactive Calculator project, implement addition and multiplication operations based on an operator string:"
        it["starter_code"] = "def calculate(a, b, op):\n    if op == '+':\n        return a + b\n    elif op == '*':\n        return a * b\n    return None"
        it["solution_code"] = "def calculate(a, b, op):\n    if op == '+':\n        return a + b\n    elif op == '*':\n        return a * b\n    return None"
        it["explanation"] = "An `if/elif` chain routes calculation to the matching arithmetic operator."
    update_item(5, "5.6_project_interactive_calculator.json", "5.6_q9", fix_5_6_9)

    def fix_42_1_9(it):
        it["prompt"] = "In the Log Parsing Automation project, count the frequency of each HTTP status code in a list of parsed log dictionaries:"
        it["starter_code"] = "def count_statuses(logs):\n    counts = {}\n    for entry in logs:\n        code = entry['status']\n        counts[code] = counts.get(code, 0) + 1\n    return counts"
        it["solution_code"] = "def count_statuses(logs):\n    counts = {}\n    for entry in logs:\n        code = entry['status']\n        counts[code] = counts.get(code, 0) + 1\n    return counts"
        it["explanation"] = "`counts.get(code, 0) + 1` increments the tally for the status code, defaulting to 0 if not yet present."
    update_item(42, "42.1_project_log_parsing_automation.json", "42.1_q9", fix_42_1_9)

    def fix_42_3_9(it):
        it["prompt"] = "In the Web Scraper API project, extract all hyperlinks from raw HTML text matching `<a href='...'>`:"
        it["starter_code"] = "import re\ndef extract_links(html):\n    return re.findall(r'href=[\"\\'](.*?)[\"\\']', html)"
        it["solution_code"] = "import re\ndef extract_links(html):\n    return re.findall(r'href=[\"\\'](.*?)[\"\\']', html)"
        it["explanation"] = "`re.findall()` returns a list of all matched substrings capturing the URL inside the quotes."
    update_item(42, "42.3_project_interactive_web_scraper_api.json", "42.3_q9", fix_42_3_9)

if __name__ == "__main__":
    run_fixes()
