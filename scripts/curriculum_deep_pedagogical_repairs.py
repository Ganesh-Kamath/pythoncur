"""
Targeted pedagogical repairs for remaining duplicate prompts, micro-lesson formatting,
and coding exercise types across all 43 units.
"""

import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CONTENT_DIR = WORKSPACE / "python_content"

TARGETED_REPAIRS = {
    # 4.1_q28: convert type to write_the_code
    ("unit_04", "4.1_the_input_function.json", "4.1_q28"): {
        "type": "write_the_code",
        "skill": "application",
        "difficulty": "hard",
        "prompt": "Write code to ask the user 'Proceed? (y/n): ' and print 'Confirmed' if they enter 'y' or 'Y', or 'Cancelled' otherwise:",
        "starter_code": "ans = input('Proceed? (y/n): ').strip().lower()\nif ans == 'y':\n    ___",
        "solution_code": "ans = input('Proceed? (y/n): ').strip().lower()\nif ans == 'y':\n    print('Confirmed')\nelse:\n    print('Cancelled')",
        "test_cases": [{"input": "", "expected_output": "Confirmed", "description": "handles y confirmation"}],
        "explanation": "Normalizing user input with `.strip().lower()` handles unexpected whitespace and case differences gracefully before branching."
    },
    # 4.2_q28: convert type to write_the_code
    ("unit_04", "4.2_processing_numeric_input.json", "4.2_q28"): {
        "type": "write_the_code",
        "skill": "application",
        "difficulty": "hard",
        "prompt": "Write code that attempts to convert `user_str` to an integer, assigning `0` if a `ValueError` occurs:",
        "starter_code": "user_str = 'invalid'\ntry:\n    val = int(user_str)\nexcept ValueError:\n    val = ___",
        "solution_code": "user_str = 'invalid'\ntry:\n    val = int(user_str)\nexcept ValueError:\n    val = 0",
        "test_cases": [{"input": "", "expected_output": "0", "description": "handles ValueError fallback"}],
        "explanation": "Using try...except ValueError is the idiomatic Python way (EAFP) to handle unpredictable numeric inputs safely."
    },
    # 41.2_q28: convert type to write_the_code
    ("unit_41", "41.2_recognizing_when_to_use_sliding_window.json", "41.2_q28"): {
        "type": "write_the_code",
        "skill": "application",
        "difficulty": "hard",
        "prompt": "A server records request latencies in milliseconds. Write a sliding window function that detects whether any consecutive window of `k` requests had an average latency exceeding `threshold`:",
        "starter_code": "def alert_latency_spike(latencies, k, threshold):\n    # Return True if any window of size k exceeds average threshold\n    pass",
        "solution_code": "def alert_latency_spike(latencies, k, threshold):\n    if len(latencies) < k or k <= 0:\n        return False\n    curr_sum = sum(latencies[:k])\n    if curr_sum / k > threshold:\n        return True\n    for i in range(k, len(latencies)):\n        curr_sum += latencies[i] - latencies[i - k]\n        if curr_sum / k > threshold:\n            return True\n    return False",
        "test_cases": [{"input": "[100, 200, 300, 800, 900], 2, 500", "expected_output": "True", "description": "detects latency spike window"}],
        "explanation": "Rolling window aggregation updates sums in O(1) per step, yielding overall O(n) execution without recalculating window sums."
    },
    # 30.6_q1: fix micro_lesson title & content
    ("unit_30", "30.6_testing_a_solution.json", "30.6_q1"): {
        "title": "Systematic Solution Testing Methodology",
        "content": "Testing is not merely running code once with the example input. A professional testing workflow follows four rigorous stages:\n\n1. **Happy Path:** Verify standard valid inputs with known answers.\n2. **Boundary Values:** Test extrema (e.g. empty lists `[]`, zero `0`, negative numbers, 1-element collections).\n3. **Failure Invariants:** Verify that invalid inputs raise the expected exceptions cleanly.\n4. **Scale & Stress:** Confirm performance and memory limits do not trigger timeouts or stack overflows.",
        "explanation": "Mastering systematic test categorization ensures no silent edge-case regressions reach production."
    },
    # 30.6_q3: fix micro_lesson title & content
    ("unit_30", "30.6_testing_a_solution.json", "30.6_q3"): {
        "title": "Test Triangulation and Defect Localization",
        "content": "When a test fails, do not guess at the fix:\n\n1. **Reproduce Minimally:** Reduce the failing input to the smallest possible test case that triggers the defect.\n2. **Isolate State:** Form a testable hypothesis about which variable or condition diverges from the specification.\n3. **Assert Invariant:** Write an explicit failing assertion capturing the bug before modifying any implementation code.",
        "explanation": "Writing an assertion that reproduces the bug before fixing it ensures proof of defect and prevents regression."
    },
    # 5.5_q10: deduplicate prompt
    ("unit_05", "5.5_truthiness.json", "5.5_q10"): {
        "prompt": "When evaluating collection containers, which of the following expressions evaluates to False in a boolean context?",
        "options": [
            "An empty list []",
            "The number 1",
            "A non-empty string 'hello'",
            "The boolean True"
        ],
        "correct_answer": "An empty list []",
        "explanation": "In Python, empty collections (empty list [], empty tuple (), empty dict {}) evaluate to False in a boolean context."
    },
    # 5.6_q6: deduplicate prompt
    ("unit_05", "5.6_project_interactive_calculator.json", "5.6_q6"): {
        "prompt": "Order the instructions to construct an interactive input prompt for two operands and an operator:",
        "options": [
            "a = float(input('First number: '))",
            "op = input('Operator (+, -, *, /): ').strip()",
            "b = float(input('Second number: '))",
            "print(f'Calculating {a} {op} {b}')"
        ],
        "correct_answer": [
            "a = float(input('First number: '))",
            "op = input('Operator (+, -, *, /): ').strip()",
            "b = float(input('Second number: '))",
            "print(f'Calculating {a} {op} {b}')"
        ],
        "explanation": "Reading inputs in logical sequence gathers all parameters before printing the execution summary."
    },
    # 5.6_q25-q30: calculator project milestones
    ("unit_05", "5.6_project_interactive_calculator.json", "5.6_q25"): {
        "prompt": "Calculator Milestone 13: Implement memory storage functions: write `Memory` helper class supporting `store(val)`, `recall()`, and `clear()`.",
        "starter_code": "class CalculatorMemory:\n    def __init__(self):\n        self.val = 0\n    def store(self, n):\n        self.val = n\n    def recall(self):\n        return self.val\n    def clear(self):\n        self.val = 0",
        "solution_code": "class CalculatorMemory:\n    def __init__(self):\n        self.val = 0\n    def store(self, n):\n        self.val = n\n    def recall(self):\n        return self.val\n    def clear(self):\n        self.val = 0",
        "test_cases": [{"input": "", "expected_output": "0", "description": "memory initialized to 0"}],
        "explanation": "Encapsulating memory state within a dedicated class provides clean state management without polluting global scope."
    },
    ("unit_05", "5.6_project_interactive_calculator.json", "5.6_q26"): {
        "prompt": "Calculator Milestone 14: Debug floating-point formatting: fix numeric precision output by formatting results to 2 decimal places.",
        "starter_code": "def format_result(val):\n    # Return formatted string with 2 decimal places\n    return str(val)",
        "solution_code": "def format_result(val):\n    return f\"{val:.2f}\"",
        "test_cases": [{"input": "0.1 + 0.2", "expected_output": "'0.30'", "description": "formats float precision"}],
        "explanation": "Using f-string formatting specifiers `{val:.2f}` rounds and displays numbers cleanly for user interfaces."
    },
    ("unit_05", "5.6_project_interactive_calculator.json", "5.6_q27"): {
        "prompt": "Calculator Milestone 15: Predict the outcome when an interactive session checks whether the user entered an exit command:\n```python\ncmd = ' QUIT '.strip().lower()\nprint(cmd in ('q', 'quit', 'exit'))\n```",
        "options": ["True", "False", "None", "ValueError"],
        "correct_answer": "True",
        "explanation": "Stripping and lowercasing converts ' QUIT ' to 'quit', which is present in the exit command tuple, evaluating to True."
    },
    ("unit_05", "5.6_project_interactive_calculator.json", "5.6_q28"): {
        "prompt": "Calculator Milestone 16: Implement calculation history: write `log_calculation(history, a, op, b, res)` that appends formatted record string.",
        "starter_code": "def log_calculation(history, a, op, b, res):\n    # Append '{a} {op} {b} = {res}' to history list\n    pass",
        "solution_code": "def log_calculation(history, a, op, b, res):\n    history.append(f\"{a} {op} {b} = {res}\")\n    return history",
        "test_cases": [{"input": "[], 10, '+', 5, 15", "expected_output": "['10 + 5 = 15']", "description": "logs calculation history"}],
        "explanation": "Maintaining an audit log of past calculations in an append-only list enables history inspection."
    },
    ("unit_05", "5.6_project_interactive_calculator.json", "5.6_q29"): {
        "prompt": "Calculator Milestone 17: Refactor operator branching into a clean dictionary dispatch table `OPERATORS = {'+': add, '-': sub, '*': mul, '/': div}`.",
        "starter_code": "def dispatch_op(op, a, b):\n    ops = {'+': lambda x, y: x + y, '-': lambda x, y: x - y}\n    # Return operation result or None if op invalid\n    pass",
        "solution_code": "def dispatch_op(op, a, b):\n    ops = {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y}\n    handler = ops.get(op)\n    return handler(a, b) if handler else None",
        "test_cases": [{"input": "'+', 7, 3", "expected_output": "10", "description": "dispatches addition"}],
        "explanation": "Dispatch tables replace complex if-elif chains with O(1) dictionary key lookups, improving maintainability."
    },
    ("unit_05", "5.6_project_interactive_calculator.json", "5.6_q30"): {
        "prompt": "Calculator Boss Milestone: Build the complete `run_calculator(expression_str)` engine that tokenizes, evaluates operations, and formats the output string cleanly.",
        "starter_code": "def run_calculator(expr):\n    # Parse 'a op b' expression and return result\n    pass",
        "solution_code": "def run_calculator(expr):\n    parts = expr.strip().split()\n    if len(parts) != 3:\n        return 'Error: Invalid format'\n    try:\n        a, op, b = float(parts[0]), parts[1], float(parts[2])\n    except ValueError:\n        return 'Error: Invalid numbers'\n    if op == '+': return f\"{a + b:.2f}\"\n    elif op == '-': return f\"{a - b:.2f}\"\n    elif op == '*': return f\"{a * b:.2f}\"\n    elif op == '/':\n        if b == 0: return 'Error: Division by zero'\n        return f\"{a / b:.2f}\"\n    return 'Error: Invalid operator'",
        "test_cases": [{"input": "'10 / 2'", "expected_output": "'5.00'", "description": "runs complete calculator engine"}],
        "explanation": "This complete capstone orchestrates input validation, parsing, error recovery, arithmetic dispatch, and clean output formatting."
    },
    # 7.5_q30: deduplicate prompt
    ("unit_07", "7.5_string_methods_lower_upper_strip.json", "7.5_q30"): {
        "prompt": "Advanced String Transformation: Implement a robust slugify function `to_url_slug(text)` that lowercases text, strips surrounding punctuation, and replaces internal spaces with hyphens.",
        "starter_code": "def to_url_slug(text):\n    # Return cleaned slug string\n    pass",
        "solution_code": "def to_url_slug(text):\n    return '-'.join(text.strip().lower().split())",
        "test_cases": [{"input": "'  Python Mastery Guide  '", "expected_output": "'python-mastery-guide'", "description": "slugifies text"}],
        "explanation": "Combining .strip(), .lower(), and .split() with '-'.join() cleans and standardizes arbitrary text for URL slugs."
    },
    # 7.9_q6: deduplicate prompt
    ("unit_07", "7.9_project_string_formatter.json", "7.9_q6"): {
        "prompt": "Order the steps to assemble an address formatting pipeline from raw street, city, and zip components:",
        "options": [
            "street = raw_street.strip().title()",
            "city = raw_city.strip().title()",
            "zip_code = raw_zip.strip()",
            "full_address = f'{street}, {city} {zip_code}'"
        ],
        "correct_answer": [
            "street = raw_street.strip().title()",
            "city = raw_city.strip().title()",
            "zip_code = raw_zip.strip()",
            "full_address = f'{street}, {city} {zip_code}'"
        ],
        "explanation": "Sanitizing each field individually before assembling the composite address string ensures consistent formatting."
    },
    # 9.6_q30: deduplicate prompt
    ("unit_09", "9.6_set_operations_union_intersection_difference.json", "9.6_q30"): {
        "prompt": "Complex Set Algebra: Given sets representing permissions for user roles, compute the set of permissions exclusive to admin and manager but absent in guest.",
        "starter_code": "def get_privileged_perms(admin, manager, guest):\n    # Return (admin | manager) - guest\n    pass",
        "solution_code": "def get_privileged_perms(admin, manager, guest):\n    return (admin | manager) - guest",
        "test_cases": [{"input": "{'read', 'write', 'delete'}, {'read', 'write'}, {'read'}", "expected_output": "{'write', 'delete'}", "description": "set difference of union"}],
        "explanation": "Union `|` gathers all permissions across both privileged roles, and difference `-` excludes any general guest permissions."
    },
    # 10.4_q26: deduplicate prompt
    ("unit_10", "10.4_deleting_key_value_pairs.json", "10.4_q26"): {
        "prompt": "Safe Dictionary Key Removal: Fix this deletion routine so deleting a non-existent key from a configuration dict uses `.pop(key, None)` instead of crashing with `KeyError`.",
        "starter_code": "def remove_session(data, session_id):\n    # Prevent KeyError on missing session_id\n    del data[session_id]\n    return data",
        "solution_code": "def remove_session(data, session_id):\n    data.pop(session_id, None)\n    return data",
        "test_cases": [{"input": "{'user1': 100}, 'user2'", "expected_output": "{'user1': 100}", "description": "safely pops non-existent key"}],
        "explanation": "Passing a default argument to `.pop(key, None)` safely deletes existing keys while preventing KeyError when the key is absent."
    },
    # 10.4_q30: deduplicate prompt
    ("unit_10", "10.4_deleting_key_value_pairs.json", "10.4_q30"): {
        "prompt": "Batch Dictionary Key Deletion: Write a function `remove_keys(d, keys_to_remove)` that mutates `d` in-place, removing each key in `keys_to_remove` without raising errors for missing keys.",
        "starter_code": "def remove_keys(d, keys_to_remove):\n    # Remove each key in keys_to_remove safely\n    pass",
        "solution_code": "def remove_keys(d, keys_to_remove):\n    for k in keys_to_remove:\n        d.pop(k, None)\n    return d",
        "test_cases": [{"input": "{'a': 1, 'b': 2, 'c': 3}, ['a', 'z']", "expected_output": "{'b': 2, 'c': 3}", "description": "batch safe key deletion"}],
        "explanation": "Iterating over keys to remove and calling `.pop(k, None)` ensures idempotent, exception-free dictionary trimming."
    },
    # 12.1_q28: deduplicate prompt
    ("unit_12", "12.1_syntax_errors_vs_runtime_errors.json", "12.1_q28"): {
        "prompt": "Syntax vs Runtime Discrimination: Given four code snippets, identify which snippet fails during the parsing/compilation stage before any code executes.",
        "options": [
            "for i in range(5) print(i)",
            "print(10 / 0)",
            "print(undefined_variable_name)",
            "int('invalid_number_string')"
        ],
        "correct_answer": "for i in range(5) print(i)",
        "explanation": "Missing a colon in a for statement violates Python grammar and raises SyntaxError during compilation, preventing execution."
    },
    # 12.1_q30: deduplicate prompt
    ("unit_12", "12.1_syntax_errors_vs_runtime_errors.json", "12.1_q30"): {
        "prompt": "Error Classification Challenge: Implement an exception classifier `classify_code(code_snippet)` that distinguishes compile-time SyntaxError from runtime errors.",
        "starter_code": "def classify_code(snippet):\n    # Return 'syntax_error', 'runtime_error', or 'ok'\n    pass",
        "solution_code": "def classify_code(snippet):\n    try:\n        compiled = compile(snippet, '<string>', 'exec')\n    except SyntaxError:\n        return 'syntax_error'\n    try:\n        exec(compiled, {})\n        return 'ok'\n    except Exception:\n        return 'runtime_error'",
        "test_cases": [{"input": "'x = 10 / 0'", "expected_output": "'runtime_error'", "description": "detects runtime ZeroDivisionError"}],
        "explanation": "The built-in compile() function isolates syntax parsing from runtime execution via exec()."
    },
    # 18.3_q30: deduplicate prompt
    ("unit_18", "18.3_raising_exceptions.json", "18.3_q30"): {
        "prompt": "Custom Exception Hierarchy: Design a domain-specific `NegativeValueError(ValueError)` subclass and write `validate_positive(val)` that raises it when `val < 0`.",
        "starter_code": "class NegativeValueError(ValueError):\n    pass\n\ndef validate_positive(val):\n    # Raise NegativeValueError if val < 0\n    pass",
        "solution_code": "class NegativeValueError(ValueError):\n    pass\n\ndef validate_positive(val):\n    if val < 0:\n        raise NegativeValueError('Value must be positive')\n    return val",
        "test_cases": [{"input": "5", "expected_output": "5", "description": "positive value passes validation"}],
        "explanation": "Subclassing standard exception classes creates expressive, catchable domain error types."
    },
    # 19.3_q30: deduplicate prompt
    ("unit_19", "19.3_basic_patterns_and_matching.json", "19.3_q30"): {
        "prompt": "Regex Pattern Extraction: Write a function `extract_hashtags(post)` that finds and returns all unique hashtags (words starting with `#`) in a social media caption.",
        "starter_code": "import re\ndef extract_hashtags(post):\n    # Return list of hashtags\n    pass",
        "solution_code": "import re\ndef extract_hashtags(post):\n    return re.findall(r'#\\w+', post)",
        "test_cases": [{"input": "'Hello #python and #coding world!'", "expected_output": "['#python', '#coding']", "description": "extracts hashtags with re.findall"}],
        "explanation": "The regex `#\\w+` matches a literal hash followed by one or more alphanumeric word characters."
    },
    # 19.4_q30: deduplicate prompt
    ("unit_19", "19.4_character_classes_and_quantifiers.json", "19.4_q30"): {
        "prompt": "Quantifier Boundary Testing: Write a regex validation function `is_valid_hex_color(code)` that strictly matches 3-digit or 6-digit hex color codes with a leading `#`.",
        "starter_code": "import re\ndef is_valid_hex_color(code):\n    # Match #FFF or #FFFFFF exactly\n    pass",
        "solution_code": "import re\ndef is_valid_hex_color(code):\n    return bool(re.fullmatch(r'#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})', code))",
        "test_cases": [{"input": "'#A3F'", "expected_output": "True", "description": "matches valid 3-char hex code"}],
        "explanation": "Using re.fullmatch with non-capturing group and exact quantifiers `{3}` and `{6}` ensures no extraneous characters pass validation."
    },
    # 21.1_q28: deduplicate prompt
    ("unit_21", "21.1_class_attributes_vs_instance_attributes.json", "21.1_q28"): {
        "prompt": "Class vs Instance State Audit: Write a function `has_instance_override(obj, attr_name)` that returns `True` if `attr_name` exists in `obj.__dict__`.",
        "starter_code": "def has_instance_override(obj, attr_name):\n    # Return True if attribute was assigned directly to instance\n    pass",
        "solution_code": "def has_instance_override(obj, attr_name):\n    return attr_name in obj.__dict__",
        "test_cases": [{"input": "type('Test', (), {'val': 10})(), 'val'", "expected_output": "False", "description": "class attribute is not in instance dict"}],
        "explanation": "Attributes stored in instance `__dict__` override class-level defaults during attribute resolution (MRO)."
    },
    # 21.1_q30: deduplicate prompt
    ("unit_21", "21.1_class_attributes_vs_instance_attributes.json", "21.1_q30"): {
        "prompt": "Dynamic Class Attribute Architecture: Design a class `Config` where class attributes serve as global defaults and instance attributes serve as per-request overrides.",
        "starter_code": "class Config:\n    timeout = 30\n    def __init__(self, timeout=None):\n        if timeout is not None:\n            self.timeout = timeout",
        "solution_code": "class Config:\n    timeout = 30\n    def __init__(self, timeout=None):\n        if timeout is not None:\n            self.timeout = timeout",
        "test_cases": [{"input": "", "expected_output": "30", "description": "instance uses class default when not overridden"}],
        "explanation": "This pattern allows instances to fallback to shared class defaults while supporting local instance overrides."
    },
    # 25.5_q27: deduplicate prompt
    ("unit_25", "25.5_web_scraping_basics.json", "25.5_q27"): {
        "prompt": "Safe Tag Extraction: Write a function `safe_get_text(tag)` that returns stripped text if tag is not None, or empty string otherwise.",
        "starter_code": "def safe_get_text(tag):\n    # Return stripped text or '' if tag is None\n    pass",
        "solution_code": "def safe_get_text(tag):\n    return tag.get_text().strip() if tag else ''",
        "test_cases": [{"input": "None", "expected_output": "''", "description": "returns empty string for missing tag"}],
        "explanation": "Guarding against None when searching HTML soup prevents AttributeError crashes when elements are absent."
    },
    # 33.3_q30: deduplicate prompt
    ("unit_33", "33.3_sets_for_fast_lookups.json", "33.3_q30"): {
        "prompt": "Fast Set Lookups: Write a function `find_common_interests(user_a_tags, user_b_tags)` that finds common elements in O(min(len(a), len(b))) average time.",
        "starter_code": "def find_common_interests(tags_a, tags_b):\n    # Return set intersection in optimal time\n    pass",
        "solution_code": "def find_common_interests(tags_a, tags_b):\n    return set(tags_a) & set(tags_b)",
        "test_cases": [{"input": "['python', 'ml', 'web'], ['web', 'rust', 'python']", "expected_output": "{'python', 'web'}", "description": "finds common tags"}],
        "explanation": "Set intersection operator `&` leverages hash table lookups to achieve optimal intersection."
    },
    # 34.3_q30: deduplicate prompt
    ("unit_34", "34.3_valid_parentheses_and_history_problems.json", "34.3_q30"): {
        "prompt": "Undo/Redo History Engine: Implement an `ActionHistory` class using two stacks supporting `perform_action(act)`, `undo()`, and `redo()`.",
        "starter_code": "class ActionHistory:\n    def __init__(self):\n        self.undo_stack = []\n        self.redo_stack = []\n    def perform(self, act):\n        self.undo_stack.append(act)\n        self.redo_stack.clear()\n    def undo(self):\n        if self.undo_stack:\n            act = self.undo_stack.pop()\n            self.redo_stack.append(act)\n            return act\n        return None",
        "solution_code": "class ActionHistory:\n    def __init__(self):\n        self.undo_stack = []\n        self.redo_stack = []\n    def perform(self, act):\n        self.undo_stack.append(act)\n        self.redo_stack.clear()\n    def undo(self):\n        if self.undo_stack:\n            act = self.undo_stack.pop()\n            self.redo_stack.append(act)\n            return act\n        return None",
        "test_cases": [{"input": "", "expected_output": "None", "description": "undo on empty history returns None"}],
        "explanation": "Two complementary LIFO stacks model undo/redo workflows with O(1) push and pop operations."
    },
    # 35.1_q28: deduplicate prompt
    ("unit_35", "35.1_linked_list_nodes.json", "35.1_q28"): {
        "prompt": "Linked List Cycle Detection: Implement Floyd's cycle-finding algorithm (`has_cycle(head)`) using fast and slow pointers.",
        "starter_code": "def has_cycle(head):\n    # Return True if linked list contains a cycle\n    pass",
        "solution_code": "def has_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            return True\n    return False",
        "test_cases": [{"input": "None", "expected_output": "False", "description": "empty list has no cycle"}],
        "explanation": "Fast pointer advancing 2 steps while slow pointer advances 1 step guarantees collision in O(n) time if a cycle exists."
    },
    # 36.4_q28: deduplicate prompt
    ("unit_36", "36.4_recursion_vs_iteration.json", "36.4_q28"): {
        "prompt": "Recursion to Iteration Conversion: Convert recursive countdown into an explicit iterative stack-based countdown avoiding recursion limits.",
        "starter_code": "def countdown_iterative(n):\n    # Return list of numbers from n down to 1 iteratively\n    pass",
        "solution_code": "def countdown_iterative(n):\n    res = []\n    stack = [n]\n    while stack:\n        curr = stack.pop()\n        if curr > 0:\n            res.append(curr)\n            stack.append(curr - 1)\n    return res",
        "test_cases": [{"input": "3", "expected_output": "[3, 2, 1]", "description": "counts down iteratively"}],
        "explanation": "Replacing implicit call frames with an explicit heap-allocated list stack prevents RecursionError."
    },
    # 38.5_q28: deduplicate prompt
    ("unit_38", "38.5_recursion_with_trees.json", "38.5_q28"): {
        "prompt": "Tree Maximum Depth: Implement recursive `max_depth(root)` returning the number of nodes along the longest path from root to leaf.",
        "starter_code": "def max_depth(root):\n    # Return max depth of binary tree\n    pass",
        "solution_code": "def max_depth(root):\n    if not root:\n        return 0\n    return 1 + max(max_depth(root.left), max_depth(root.right))",
        "test_cases": [{"input": "None", "expected_output": "0", "description": "empty tree has depth 0"}],
        "explanation": "The maximum depth of a binary tree is 1 plus the maximum of the depths of its left and right subtrees."
    },
    # 38.5_q30: deduplicate prompt
    ("unit_38", "38.5_recursion_with_trees.json", "38.5_q30"): {
        "prompt": "Binary Tree Path Sum: Implement `has_path_sum(root, target)` checking if there is a root-to-leaf path summing to target.",
        "starter_code": "def has_path_sum(root, target):\n    # Return True if any root-to-leaf path sums to target\n    pass",
        "solution_code": "def has_path_sum(root, target):\n    if not root:\n        return False\n    if not root.left and not root.right:\n        return root.val == target\n    rem = target - root.val\n    return has_path_sum(root.left, rem) or has_path_sum(root.right, rem)",
        "test_cases": [{"input": "None, 10", "expected_output": "False", "description": "empty tree has no path"}],
        "explanation": "Subtracting node value along recursive subpaths terminates when a leaf node matches the remaining balance."
    },
    # 39.5_q30: deduplicate prompt
    ("unit_39", "39.5_visited_tracking_and_connected_components.json", "39.5_q30"): {
        "prompt": "Connected Components in Grid: Implement `count_islands(grid)` using visited tracking to count distinct islands of 1s in a 2D matrix.",
        "starter_code": "def count_islands(grid):\n    # Return count of connected 1s in grid\n    pass",
        "solution_code": "def count_islands(grid):\n    if not grid:\n        return 0\n    rows, cols = len(grid), len(grid[0])\n    visited = set()\n    def dfs(r, c):\n        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:\n            return\n        visited.add((r, c))\n        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n            dfs(r + dr, c + dc)\n    count = 0\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == 1 and (r, c) not in visited:\n                dfs(r, c)\n                count += 1\n    return count",
        "test_cases": [{"input": "[[1, 1, 0], [0, 1, 0], [0, 0, 1]]", "expected_output": "2", "description": "counts 2 separate islands"}],
        "explanation": "DFS explores each connected island completely, tracking visited coordinates to ensure each island is counted exactly once."
    }
}

def apply_targeted_repairs():
    print("Applying targeted pedagogical repairs...")
    count = 0
    for (udir, fname, item_id), patch in TARGETED_REPAIRS.items():
        fpath = CONTENT_DIR / udir / fname
        if not fpath.exists():
            print(f"File not found: {fpath}")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        found = False
        for it in data.get("items", []):
            if it.get("id") == item_id:
                it.update(patch)
                found = True
                count += 1
                break
        
        if found:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Applied {count} targeted pedagogical repairs.")

if __name__ == "__main__":
    apply_targeted_repairs()
