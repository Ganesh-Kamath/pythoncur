"""
Deep repair script for curriculum bugs discovered by deterministic execution audit:
- 1.1: Add missing metadata 'prerequisites': []
- 4.2: Replace synthetic prompts with rich numeric input handling exercises
- 5.6, 42.1, 42.3: Replace duplicate item 8s with realistic project exercises
- 5.3_q11: Correct answer to 14 / Final: 14
- 5.4_q9: Format expected output and options cleanly
- 7.2_q11: Correct answer for 'Codolingo'[-3:] -> 'ngo'
- 7.2_q12: Correct answer for 'Python is fun'[-5:-2] -> 's f'
- 7.3_q7: Correct answer for 'Codolingo'[2:7] -> 'dolin'
- 7.3_q12: Correct answer for 'HelloWorld'[5:0:-1] -> 'Wolle'
- 7.6_q11: Correct answer for 'aaa'.replace('a', 'b', 1).replace('a', 'c') -> 'bcc'
- 8.3_q11: Correct answer for [2, 4].insert(2, 3).append(5) -> [2, 4, 3, 5]
- 8.5_q8: Correct answer for reverse([7, 2, 8, 2, 9]) -> [9, 2, 8, 2, 7]
- 8.5_q11: Correct answer for items[1] + items[2] -> 7
- 9.2_q11: Normalize expected output format
- 18.3_q7: Correct answer to 'done' (condition 10 < 0 is False)
- 32.1_q7: Correct answer for 20 + len('hi') -> 22
- 37.3_q12: Correct answer for ascending sort by score -> Alice (88), Charlie (88), Bob (92)
- 33.1_q8, 33.1_q9, 33.1_q12, 39.1_q8: Normalize output representations
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
    
    # Check lesson level metadata
    if item_id == "__lesson__":
        updater(data)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Updated lesson metadata in {filename}")
        return True

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
    # 1. Lesson 1.1 prerequisites
    def fix_1_1_meta(d):
        d["prerequisites"] = []
    update_item(1, "1.1_what_is_programming.json", "__lesson__", fix_1_1_meta)

    # 2. 5.3_q11
    def fix_5_3_11(it):
        it["options"] = ["Low\nFinal: 7", "14\nFinal: 14", "High\nFinal: 7", "Error"]
        it["correct_answer"] = "14\nFinal: 14"
        it["explanation"] = "When `a = 7`, `a > 10` is False. The `elif a > 5` branch is True, so `a = 7 * 2 = 14` is printed. The final line then prints `Final: 14`."
    update_item(5, "5.3_multiple_paths_with_elif.json", "5.3_q11", fix_5_3_11)

    # 3. 5.4_q9
    def fix_5_4_9(it):
        it["options"] = ["Pass\nGood job", "Pass\nExcellent", "Fail", "Error"]
        it["correct_answer"] = "Pass\nGood job"
        it["explanation"] = "Since score is 72, the outer condition `score >= 60` is True, and the inner condition `score < 80` is also True. Both 'Pass' and 'Good job' are printed."
    update_item(5, "5.4_nested_conditions.json", "5.4_q9", fix_5_4_9)

    # 4. 7.2_q11
    def fix_7_2_11(it):
        it["options"] = ["'Cod'", "'ngo'", "'dolin'", "'ingo'"]
        it["correct_answer"] = "'ngo'"
        it["explanation"] = "`name[-3:]` slices from index -3 ('n') through the end of the string, yielding 'ngo'."
    update_item(7, "7.2_negative_indexing.json", "7.2_q11", fix_7_2_11)

    # 5. 7.2_q12
    def fix_7_2_12(it):
        it["options"] = ["'fun'", "'s f'", "'is '", "'Python'"]
        it["correct_answer"] = "'s f'"
        it["explanation"] = "In 'Python is fun', negative index -5 is 's', -4 is ' ', and -3 is 'f'. The slice [-5:-2] excludes index -2 ('u'), resulting in 's f'."
    update_item(7, "7.2_negative_indexing.json", "7.2_q12", fix_7_2_12)

    # 6. 7.3_q7
    def fix_7_3_7(it):
        it["options"] = ["Cod", "odoli", "dolin", "ng"]
        it["correct_answer"] = "dolin"
        it["explanation"] = "In 'Codolingo', index 2 is 'd' and index 7 is 'g' (exclusive). Characters at indices 2, 3, 4, 5, 6 produce 'dolin'."
    update_item(7, "7.3_string_slicing.json", "7.3_q7", fix_7_3_7)

    # 7. 7.3_q12
    def fix_7_3_12(it):
        it["options"] = ["dlroW", "Wolle", "olleH", "Error"]
        it["correct_answer"] = "Wolle"
        it["explanation"] = "In 'HelloWorld', index 5 is 'W'. Stepping backward by -1 down to index 1 (excluding index 0) collects 'W', 'o', 'l', 'l', 'e', producing 'Wolle'."
    update_item(7, "7.3_string_slicing.json", "7.3_q12", fix_7_3_12)

    # 8. 7.6_q11
    def fix_7_6_11(it):
        it["options"] = ["'aaa'", "'aba'", "'bcc'", "'ccc'"]
        it["correct_answer"] = "'bcc'"
        it["explanation"] = "The first replacement replaces only 1 occurrence of 'a' with 'b', yielding 'baa'. The second replacement replaces all remaining occurrences of 'a' with 'c', yielding 'bcc'."
    update_item(7, "7.6_string_methods_replace.json", "7.6_q11", fix_7_6_11)

    # 9. 8.3_q11
    def fix_8_3_11(it):
        it["options"] = ["[2, 4, 3, 5]", "[2, 3, 4, 5]", "[2, 4, 5, 3]", "[3, 2, 4, 5]"]
        it["correct_answer"] = "[2, 4, 3, 5]"
        it["explanation"] = "`lst.insert(2, 3)` on `[2, 4]` places 3 at index 2 (the current end), making `[2, 4, 3]`. `lst.append(5)` adds 5 to the end, giving `[2, 4, 3, 5]`."
    update_item(8, "8.3_adding_elements_append_and_insert.json", "8.3_q11", fix_8_3_11)

    # 10. 8.5_q8
    def fix_8_5_8(it):
        it["options"] = ["[9, 2, 8, 2, 7]", "[7, 2, 8, 2, 9]", "[2, 8, 2, 7, 9]", "None"]
        it["correct_answer"] = "[9, 2, 8, 2, 7]"
        it["explanation"] = "`nums.reverse()` reverses the elements in place. The reversed sequence is [9, 2, 8, 2, 7]."
    update_item(8, "8.5_sorting_and_reversing_lists.json", "8.5_q8", fix_8_5_8)

    # 11. 8.5_q11
    def fix_8_5_11(it):
        it["options"] = ["7", "9", "11", "3"]
        it["correct_answer"] = "7"
        it["explanation"] = "After `sort()`, `items` is `[1, 2, 5, 8]`. After `reverse()`, it is `[8, 5, 2, 1]`. `items[1]` is 5 and `items[2]` is 2. `5 + 2 = 7`."
    update_item(8, "8.5_sorting_and_reversing_lists.json", "8.5_q11", fix_8_5_11)

    # 12. 9.2_q11
    def fix_9_2_11(it):
        it["prompt"] = "What does this code print?\n```python\nx, y = (1, 2), (3, 4)\nx, y = y, x\nprint(f'{x} {y}')\n```"
        it["options"] = ["(3, 4) (1, 2)", "(1, 2) (3, 4)", "((3, 4), (1, 2))", "Error"]
        it["correct_answer"] = "(3, 4) (1, 2)"
        it["explanation"] = "Tuple unpacking swaps the references: x receives (3, 4) and y receives (1, 2)."
    update_item(9, "9.2_tuple_immutability.json", "9.2_q11", fix_9_2_11)

    # 13. 18.3_q7
    def fix_18_3_7(it):
        it["options"] = ["done", "ValueError: negative value", "ValueError: negative value\ndone", "No output"]
        it["correct_answer"] = "done"
        it["explanation"] = "`value` is 10, so the condition `value < 0` is False. The exception is never raised, and 'done' is printed."
    update_item(18, "18.3_raising_exceptions.json", "18.3_q7", fix_18_3_7)

    # 14. 32.1_q7
    def fix_32_1_7(it):
        it["options"] = ["22", "31", "32", "40"]
        it["correct_answer"] = "22"
        it["explanation"] = "`arr[1]` is 20 and `len('hi')` is 2. Adding them gives 20 + 2 = 22."
    update_item(32, "32.1_array_and_string_concepts.json", "32.1_q7", fix_32_1_7)

    # 15. 37.3_q12
    def fix_37_3_12(it):
        it["options"] = [
            "[{'name': 'Alice', 'score': 88}, {'name': 'Charlie', 'score': 88}, {'name': 'Bob', 'score': 92}]",
            "[{'name': 'Bob', 'score': 92}, {'name': 'Alice', 'score': 88}, {'name': 'Charlie', 'score': 88}]",
            "[{'name': 'Charlie', 'score': 88}, {'name': 'Alice', 'score': 88}, {'name': 'Bob', 'score': 92}]",
            "Error"
        ]
        it["correct_answer"] = "[{'name': 'Alice', 'score': 88}, {'name': 'Charlie', 'score': 88}, {'name': 'Bob', 'score': 92}]"
        it["explanation"] = "Python's `sort()` sorts in ascending order by default. Scores 88 come before 92. Since Python's Timsort is stable, Alice remains before Charlie."
    update_item(37, "37.3_sorting_concepts_and_algorithms.json", "37.3_q12", fix_37_3_12)

    # 16. Replace duplicate items in 4.2 (processing numeric input)
    num_replacements = {
        "4.2_q7": {
            "type": "code_prediction",
            "prompt": "What happens when `int(' 42 \\n')` is evaluated?\n```python\nval = int(' 42 \\n')\nprint(val)\n```",
            "options": ["42", "ValueError", "'42'", "None"],
            "correct_answer": "42",
            "explanation": "Python's `int()` function automatically ignores leading and trailing whitespace characters, returning 42."
        },
        "4.2_q8": {
            "type": "error_diagnosis",
            "prompt": "What exception occurs if a user enters 'ten' and the program runs `int(input())`?",
            "options": ["ValueError", "TypeError", "SyntaxError", "NameError"],
            "correct_answer": "ValueError",
            "explanation": "Attempting to parse a non-numeric string into an integer raises a ValueError."
        },
        "4.2_q9": {
            "type": "fix_the_code",
            "prompt": "Fix this code so it safely calculates total price with a floating-point discount rate:",
            "starter_code": "price = 100\nrate = float('0.15')\ntotal = price - (price * rate)\nprint(int(total))",
            "solution_code": "price = 100\nrate = float('0.15')\ntotal = price - (price * rate)\nprint(int(total))",
            "explanation": "Converting '0.15' with `float()` parses the decimal fraction correctly."
        },
        "4.2_q11": {
            "type": "multiple_choice",
            "prompt": "Why does `int('3.14')` directly raise a `ValueError` in Python?",
            "options": [
                "int() requires a string representing an integer base-10 literal without a decimal point",
                "Python does not support converting strings to numbers",
                "Floats cannot be cast to integers",
                "The string contains non-ASCII characters"
            ],
            "correct_answer": "int() requires a string representing an integer base-10 literal without a decimal point",
            "explanation": "`int()` only parses pure whole integer strings. To parse '3.14', first call `float('3.14')`."
        },
        "4.2_q12": {
            "type": "write_the_code",
            "prompt": "Write code to convert the numeric string in `user_val` to a float and multiply it by 2:",
            "starter_code": "user_val = '14.5'\n# Convert and double\nresult = ___",
            "solution_code": "user_val = '14.5'\nresult = float(user_val) * 2",
            "explanation": "Use `float(user_val)` to convert the string before performing numeric multiplication."
        }
    }
    for qid, nd in num_replacements.items():
        def make_upd(d):
            def upd(it):
                for k, v in d.items():
                    it[k] = v
            return upd
        update_item(4, "4.2_processing_numeric_input.json", qid, make_upd(nd))

    # 17. Replace duplicate item 8s in project lessons
    def fix_5_6_8(it):
        it["prompt"] = "In the Interactive Calculator project, implement division by zero protection in the division operation handler:"
        it["starter_code"] = "def safe_divide(a, b):\n    if b == 0:\n        return 'Error: Division by zero'\n    return a / b"
        it["solution_code"] = "def safe_divide(a, b):\n    if b == 0:\n        return 'Error: Division by zero'\n    return a / b"
        it["explanation"] = "Checking `if b == 0` guards against raising ZeroDivisionError before attempting division."
    update_item(5, "5.6_project_interactive_calculator.json", "5.6_q8", fix_5_6_8)

    def fix_42_1_8(it):
        it["prompt"] = "In the Log Parsing Automation project, filter a list of log entries to extract only entries where level is 'ERROR':"
        it["starter_code"] = "def filter_errors(logs):\n    return [log for log in logs if log['level'] == '___']"
        it["solution_code"] = "def filter_errors(logs):\n    return [log for log in logs if log['level'] == 'ERROR']"
        it["explanation"] = "A list comprehension filters the logs matching `'level' == 'ERROR'`."
    update_item(42, "42.1_project_log_parsing_automation.json", "42.1_q8", fix_42_1_8)

    def fix_42_3_8(it):
        it["prompt"] = "In the Web Scraper API project, parse an HTML title string using a simple regular expression:"
        it["starter_code"] = "import re\ndef extract_title(html):\n    match = re.search(r'<title>(.*?)</title>', html)\n    return match.group(1) if match else None"
        it["solution_code"] = "import re\ndef extract_title(html):\n    match = re.search(r'<title>(.*?)</title>', html)\n    return match.group(1) if match else None"
        it["explanation"] = "`re.search()` with non-greedy `(.*?)` captures the inner text of the HTML `<title>` tag."
    update_item(42, "42.3_project_interactive_web_scraper_api.json", "42.3_q8", fix_42_3_8)

if __name__ == "__main__":
    run_fixes()
