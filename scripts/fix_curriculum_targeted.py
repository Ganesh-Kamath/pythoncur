"""
Targeted fixer for remaining curriculum audit issues:
1. Syntax fixes in 3.5_q22, 33.1_q9, 35.5_q7
2. Add '___' marker to the 12 fill_in_the_blank items lacking it
3. Replace 4.1 while/input duplicates with rich, interactive input-handling exercises
4. Replace repetitive project item 7s with unique, milestone-aligned tasks
5. Fix 38.3_q7 explanation
"""

import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PYTHON_CONTENT = WORKSPACE / "python_content"

def update_item_in_lesson(unit_num: int, lesson_filename: str, item_id: str, updater):
    unit_dir = PYTHON_CONTENT / f"unit_{unit_num:02d}"
    file_path = unit_dir / lesson_filename
    if not file_path.exists():
        print(f"Error: {file_path} not found")
        return False
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    modified = False
    for item in data.get("items", []):
        if item.get("id") == item_id:
            updater(item)
            modified = True
            break
            
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Updated {item_id} in {lesson_filename}")
        return True
    else:
        print(f"Warning: {item_id} not found in {lesson_filename}")
        return False

def fix_all():
    # 1. Syntax error in 3.5_q22
    def fix_3_5_22(it):
        it["starter_code"] = 'if role == "admin" or "moderator":\n    print("Access Granted")'
        it["solution_code"] = 'if role == "admin" or role == "moderator":\n    print("Access Granted")'
        it["explanation"] = "In Python, each condition around 'or' is evaluated separately. 'or \"moderator\"' evaluates as truthy because non-empty strings are True. You must explicitly test `role == \"moderator\"`."
    update_item_in_lesson(3, "3.5_logical_operators.json", "3.5_q22", fix_3_5_22)

    # 2. Syntax error in 33.1_q9
    def fix_33_1_9(it):
        it["prompt"] = "What is the output of the following code?\n\n```python\nht = {}\nht['x'] = 1\nht['y'] = 2\nht['z'] = 3\ndel ht['y']\nprint(ht)\nprint(ht.get('y', 'missing'))\n```"
    update_item_in_lesson(33, "33.1_hash_tables_concepts.json", "33.1_q9", fix_33_1_9)

    # 3. Syntax error in 35.5_q7
    def fix_35_5_7(it):
        it["prompt"] = "Given the following code, what value does `slow.val` hold after the loop finishes?\n\n```python\nclass Node:\n    def __init__(self, val, next=None):\n        self.val = val\n        self.next = next\n\nhead = Node(1, Node(2, Node(3, Node(4))))\nslow = head\nfast = head\n\nwhile fast and fast.next:\n    slow = slow.next\n    fast = fast.next.next\n\nprint('slow.val =', slow.val)\n```"
    update_item_in_lesson(35, "35.5_fast_and_slow_pointers.json", "35.5_q7", fix_35_5_7)

    # 4. Fill-in-the-blank items lacking '___'
    blank_fixes = {
        (11, "11.5_multiple_parameters_and_returns.json", "11.5_q13", "def calculate_area(w, h):\n    return w * h\n\n# Call the function with width 5 and height 10\narea = calculate_area(___)"),
        (13, "13.5_appending_to_files.json", "13.5_q13", "with open('notes.txt', '___') as f:\n    f.write('Python is fun!')"),
        (13, "13.5_appending_to_files.json", "13.5_q18", "with open('log.txt', 'a') as f:\n    bytes_written = f.___('entry\\n')"),
        (16, "16.6_readability_when_not_to_use_comprehensions.json", "16.6_q14", "Complete the comprehension by filling in the filtering keyword:\n`[x * 2 for x in nums ___ x > 0]`"),
        (16, "16.6_readability_when_not_to_use_comprehensions.json", "16.6_q16", "Fill in the syntax to create a set comprehension instead of a list comprehension:\n`unique_lens = ___[len(w) for w in words]___`"),
        (18, "18.2_the_else_and_finally_clauses.json", "18.2_q16", "Fill in the missing method call to ensure clean resource release:\n```python\nwith open('data.txt') as f:\n    data = f.___()\n```"),
        (20, "20.5_instance_methods.json", "20.5_q14", "class Calculator:\n    def add(___, a, b):\n        return a + b\n\ncalc = Calculator()\nresult = calc.add(2, 3)"),
        (21, "21.2_class_methods_and_static_methods.json", "21.2_q13", "Fill in the decorator for the method below so that it receives the class as its first parameter:\n\n@___\ndef from_string(cls, data_str):\n    return cls(*data_str.split(','))"),
        (24, "24.1_principles_of_clean_code.json", "24.1_q13", "Complete the statement to follow the DRY principle:\n\n___ = 0.08  # TAX_RATE\ntotal = price + (price * ___)"),
        (25, "25.6_project_api_weather_dashboard.json", "25.6_q17", "To ensure your script runs only when executed directly, place the main wiring logic inside:\n`if ___ == '__main__':`"),
        (27, "27.6_project_full_stack_to_do_api.json", "27.6_q13", "Complete the import statement to bring in the Flask class from the flask module:\n`from flask import ___`"),
        (35, "35.2_traversal.json", "35.2_q13", "Complete the traversal loop to visit every node in a singly linked list starting from head:\n```python\ncurr = head\nwhile curr is not None:\n    print(curr.val)\n    curr = curr.___\n```"),
    }
    for u_num, fname, qid, prompt_text in blank_fixes:
        def make_blank_fix(pt):
            def updater(it):
                it["prompt"] = pt
            return updater
        update_item_in_lesson(u_num, fname, qid, make_blank_fix(prompt_text))

    # 5. Fix duplicate prompts in 4.1 (input function)
    input_replacements = {
        "4.1_q7": {
            "type": "code_prediction",
            "prompt": "What is the return type of `input()`, even if the user types digits like `42`?\n```python\nage = input('Enter age: ')\nprint(type(age))\n```",
            "options": ["A. <class 'str'>", "B. <class 'int'>", "C. <class 'float'>", "D. <class 'number'>"],
            "correct_answer": "A",
            "explanation": "`input()` always returns a string (`str`). If you want an integer, you must explicitly convert it using `int(age)`."
        },
        "4.1_q8": {
            "type": "multiple_choice",
            "prompt": "What happens if a program executes `val = input()` in a standard interactive terminal?",
            "options": [
                "A. Execution pauses and waits until the user presses Enter",
                "B. Python raises an ImmediateInputError",
                "C. It returns None immediately without waiting",
                "D. It generates a random string automatically"
            ],
            "correct_answer": "A",
            "explanation": "`input()` pauses program execution and waits for the user to type input and press Enter."
        },
        "4.1_q9": {
            "type": "fix_the_code",
            "prompt": "Fix this code so that it removes surrounding whitespace from the user's input before printing it:",
            "starter_code": "name = input('Name: ').strip\nprint(f'Hello {name}')",
            "solution_code": "name = input('Name: ').strip()\nprint(f'Hello {name}')",
            "explanation": "`.strip()` is a method call and must include parentheses `()` to execute and return the cleaned string."
        },
        "4.1_q11": {
            "type": "multiple_choice",
            "prompt": "Why is it best practice to include a trailing space in an input prompt string like `input('Enter name: ')`?",
            "options": [
                "A. To prevent the user's typed text from bunching right against the prompt text",
                "B. Python syntax requires trailing spaces in string arguments",
                "C. It forces the terminal to flush its output buffer",
                "D. It automatically strips newline characters"
            ],
            "correct_answer": "A",
            "explanation": "A space after the colon in `'Enter name: '` creates clean visual separation between the prompt and the user's keystrokes in the terminal."
        },
        "4.1_q12": {
            "type": "output_prediction",
            "prompt": "What does this snippet display if the user types '  Python  ' and presses Enter?\n```python\ntext = '  Python  '.strip()\nprint(f'[{text}]')\n```",
            "options": ["A. [Python]", "B. [  Python  ]", "C. [Python  ]", "D. ['Python']"],
            "correct_answer": "A",
            "explanation": "`.strip()` removes leading and trailing whitespace characters, leaving `[Python]`."
        }
    }
    for qid, new_data in input_replacements.items():
        def make_rep(nd):
            def updater(it):
                for k, v in nd.items():
                    it[k] = v
            return updater
        update_item_in_lesson(4, "4.1_the_input_function.json", qid, make_rep(new_data))

    # 6. Fix duplicate project item 7s
    def fix_5_6_7(it):
        it["prompt"] = "In the Interactive Calculator project, implement input validation so entering 'exit' halts the main calculation loop:"
        it["starter_code"] = "user_input = input('Calc> ')\nif user_input.lower() == 'exit':\n    # Halt the loop\n    ___"
        it["solution_code"] = "user_input = input('Calc> ')\nif user_input.lower() == 'exit':\n    break"
        it["explanation"] = "The `break` statement immediately terminates the active `while` loop, allowing clean exit."
    update_item_in_lesson(5, "5.6_project_interactive_calculator.json", "5.6_q7", fix_5_6_7)

    def fix_42_1_7(it):
        it["prompt"] = "In the Log Parsing Automation project, parse the timestamp and severity level from an Apache/Nginx log line:"
        it["starter_code"] = "line = '2026-10-04 12:00:00 [ERROR] Connection timeout'\nparts = line.split(' ')\ntimestamp = f'{parts[0]} {parts[1]}'\nseverity = parts[2].strip('___')"
        it["solution_code"] = "line = '2026-10-04 12:00:00 [ERROR] Connection timeout'\nparts = line.split(' ')\ntimestamp = f'{parts[0]} {parts[1]}'\nseverity = parts[2].strip('[]')"
        it["explanation"] = "`.strip('[]')` strips both opening and closing square brackets from around the severity tag."
    update_item_in_lesson(42, "42.1_project_log_parsing_automation.json", "42.1_q7", fix_42_1_7)

    def fix_42_3_7(it):
        it["prompt"] = "In the Web Scraper API project, validate the HTTP response status code before attempting to parse response data:"
        it["starter_code"] = "def parse_page(response):\n    if response.status_code != ___:\n        raise ValueError(f'HTTP error: {response.status_code}')\n    return response.text"
        it["solution_code"] = "def parse_page(response):\n    if response.status_code != 200:\n        raise ValueError(f'HTTP error: {response.status_code}')\n    return response.text"
        it["explanation"] = "HTTP status code 200 represents 'OK' (successful request)."
    update_item_in_lesson(42, "42.3_project_interactive_web_scraper_api.json", "42.3_q7", fix_42_3_7)

    # 7. Fix 38.3_q7 explanation
    def fix_38_3_7(it):
        it["explanation"] = "In a Binary Search Tree (BST), keys smaller than the current node go to the left subtree, and keys larger go to the right subtree. Inserting 7 creates the root; 3 goes left of 7; 9 goes right of 7; 1 goes left of 3; 5 goes right of 3. Level-order or in-order traversal strictly maintains this property."
    update_item_in_lesson(38, "38.3_binary_search_trees.json", "38.3_q7", fix_38_3_7)

if __name__ == "__main__":
    fix_all()
