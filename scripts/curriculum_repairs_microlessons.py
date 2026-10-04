"""
CODOLINGO EXACT REPAIRS: MICRO-LESSON TEACHING CONTENT
Replaces formulaic 'provides essential rules' / 'stage_1 = True' micro-lessons
with rich, authentic Python pedagogical instruction.
"""

REPLACEMENTS_MICRO_LESSONS = {
    # 4.1 input()
    "4.1_q1": {
        "id": "4.1_q1",
        "type": "micro_lesson",
        "concept": "the_input_function_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "How the input() Function Operates",
        "content": "The `input()` function pauses program execution and waits for the user to type text into the terminal and press Enter.\n\nKey rules:\n1. `input()` ALWAYS returns a string (`str`), even if the user enters digits.\n2. To use the input as a number, it must be explicitly converted (cast) using `int()` or `float()`.\n\n```python\nname = input(\"What is your name? \")\nprint(f\"Hello, {name}!\")\n```",
        "explanation": "Calling input() halts execution, captures user keystrokes from standard input, and always returns the captured text as a str object.",
        "metadata": {"concept": "input_fundamentals", "skill": "recognition", "why_this_exercise_exists": "Core teaching on input() return types"}
    },
    "4.1_q3": {
        "id": "4.1_q3",
        "type": "micro_lesson",
        "concept": "the_input_function_prompts_and_cleaning",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["4.1_q2"],
        "title": "Prompts and Whitespace Hygiene",
        "content": "You can pass an optional prompt string to `input(\"Enter age: \")` which displays on screen without a trailing newline.\n\nUsers often introduce accidental spaces when typing. Calling `.strip()` removes leading and trailing whitespace:\n\n```python\nuser_code = input(\"Enter code: \").strip()\n```",
        "explanation": "Passing a prompt string keeps user entry on the same line, and strip() sanitizes extraneous surrounding whitespace.",
        "metadata": {"concept": "prompt_and_whitespace_hygiene", "skill": "recognition", "why_this_exercise_exists": "Teaches prompt design and input sanitization"}
    },

    # 4.2 Numeric Input
    "4.2_q1": {
        "id": "4.2_q1",
        "type": "micro_lesson",
        "concept": "processing_numeric_input_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Why Numeric Conversion is Mandatory",
        "content": "Because `input()` returns strings, attempting arithmetic on raw input leads to bugs or crashes:\n\n* `\"10\" + \"5\"` evaluates to `\"105\"` (string concatenation).\n* `\"10\" + 5` raises `TypeError: can only concatenate str to str`.\n\nTo perform arithmetic, you must convert the string to a number:\n\n```python\nage = int(input(\"Enter age: \"))\nnext_year = age + 1\n```",
        "explanation": "Python does not automatically coerce strings into numbers during arithmetic. Explicit type casting with int() or float() is required.",
        "metadata": {"concept": "numeric_input_casting", "skill": "recognition", "why_this_exercise_exists": "Explains why type conversion is required"}
    },
    "4.2_q3": {
        "id": "4.2_q3",
        "type": "micro_lesson",
        "concept": "processing_numeric_input_int_vs_float",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["4.2_q2"],
        "title": "Integer vs Floating-Point Input",
        "content": "Choose your conversion function based on the expected input:\n\n* `int()` parses whole numbers (e.g. `\"42\"` -> `42`). Calling `int(\"42.5\")` raises a `ValueError`!\n* `float()` parses numbers with decimals (e.g. `\"42.5\"` -> `42.5`).\n\n```python\nprice = float(input(\"Enter price: \"))\nquantity = int(input(\"Enter quantity: \"))\ntotal = price * quantity\n```",
        "explanation": "int() strictly requires base-10 integer digits, whereas float() supports decimal points.",
        "metadata": {"concept": "int_vs_float_parsing", "skill": "recognition", "why_this_exercise_exists": "Teaches proper choice between int() and float()"}
    },

    # 5.1 The if Statement
    "5.1_q1": {
        "id": "5.1_q1",
        "type": "micro_lesson",
        "concept": "the_if_statement_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Conditional Execution with if",
        "content": "The `if` statement evaluates a boolean condition. If the condition is `True`, Python executes the indented block of code below it:\n\n```python\nscore = 85\nif score >= 80:\n    print(\"Great job!\")\n```\n\nIn Python, code blocks are defined by indentation (typically 4 spaces), ending with a colon `:` at the end of the `if` line.",
        "explanation": "An if statement tests a condition and executes its indented block only when that condition evaluates to True.",
        "metadata": {"concept": "if_statement_fundamentals", "skill": "recognition", "why_this_exercise_exists": "Foundational if syntax and block rules"}
    },
    "5.1_q3": {
        "id": "5.1_q3",
        "type": "micro_lesson",
        "concept": "the_if_statement_comparisons",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["5.1_q2"],
        "title": "Comparison Operators and Boundaries",
        "content": "Conditions rely on comparison operators:\n\n* `==` (equal to) vs `!=` (not equal to)\n* `>` (greater than) vs `>=` (greater than or equal to)\n* `<` (less than) vs `<=` (less than or equal to)\n\nPay close attention to boundaries: `score > 90` excludes 90, while `score >= 90` includes 90!",
        "explanation": "Strict inequalities (> and <) exclude boundary points, whereas inclusive comparisons (>= and <=) include them.",
        "metadata": {"concept": "comparison_operator_boundaries", "skill": "recognition", "why_this_exercise_exists": "Teaches boundary condition vigilance"}
    },

    # 5.2 The else Statement
    "5.2_q1": {
        "id": "5.2_q1",
        "type": "micro_lesson",
        "concept": "the_else_statement_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Two-Way Decisions with if-else",
        "content": "An `else` block provides an alternative path when the `if` condition evaluates to `False`:\n\n```python\nbalance = 50\nprice = 75\n\nif balance >= price:\n    print(\"Purchase approved\")\nelse:\n    print(\"Insufficient funds\")\n```\n\nExactly one of the two blocks will execute; they are mutually exclusive.",
        "explanation": "The else block executes only when the preceding if condition evaluates to False.",
        "metadata": {"concept": "two_way_branching", "skill": "recognition", "why_this_exercise_exists": "Teaches mutual exclusivity in if-else"}
    },
    "5.2_q3": {
        "id": "5.2_q3",
        "type": "micro_lesson",
        "concept": "the_else_statement_syntax_rules",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["5.2_q2"],
        "title": "Syntax Rules of the else Clause",
        "content": "Remember these structural rules for `else`:\n\n1. `else:` cannot take a condition. Writing `else x > 5:` is a SyntaxError (use `elif` instead).\n2. `else:` must be aligned at the exact same indentation level as its matching `if:` statement.\n3. An `else` block must contain at least one indented statement (or `pass`).",
        "explanation": "else is unconditional and acts as the catch-all branch for an if statement.",
        "metadata": {"concept": "else_syntax_rules", "skill": "recognition", "why_this_exercise_exists": "Prevents common else syntax errors"}
    },

    # 5.6 Project: Interactive Calculator
    "5.6_q1": {
        "id": "5.6_q1",
        "type": "micro_lesson",
        "concept": "project_interactive_calculator_architecture",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Architecture of a Terminal Calculator",
        "content": "Building an interactive CLI calculator requires coordinating four key phases:\n\n1. **Input Ingestion:** Prompt the user for operands and parse into floats.\n2. **Operator Validation:** Verify the operation is one of `('+', '-', '*', '/')`.\n3. **Computation & Error Handling:** Guard against mathematical division by zero.\n4. **Display:** Present formatted results cleanly to the user.",
        "explanation": "CLI calculators decouple input collection, mathematical dispatch, and error handling into distinct stages.",
        "metadata": {"concept": "calculator_architecture", "skill": "recognition", "why_this_exercise_exists": "Architectural roadmap for calculator project"}
    },
    "5.6_q2": {
        "id": "5.6_q2",
        "type": "micro_lesson",
        "concept": "project_interactive_calculator_dispatch",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["5.6_q1"],
        "title": "Designing Operation Dispatch",
        "content": "In early Python, operation dispatch is cleanly structured with an `if-elif-else` chain:\n\n```python\nif op == \"+\":\n    result = a + b\nelif op == \"-\":\n    result = a - b\nelif op == \"*\":\n    result = a * b\nelif op == \"/\":\n    if b == 0:\n        result = \"Error: Division by zero\"\n    else:\n        result = a / b\nelse:\n    result = \"Error: Invalid operator\"\n```",
        "explanation": "An if-elif chain maps operator tokens to their corresponding arithmetic computations.",
        "metadata": {"concept": "operation_dispatch", "skill": "recognition", "why_this_exercise_exists": "Teaches operator branching in calculators"}
    },

    # 6.7 Nested Loops
    "6.7_q1": {
        "id": "6.7_q1",
        "type": "micro_lesson",
        "concept": "nested_loops_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Nested Loops and Execution Ordering",
        "content": "A nested loop is a loop inside another loop. For EVERY single iteration of the outer loop, the inner loop executes completely from start to finish:\n\n```python\nfor i in range(2):\n    for j in range(3):\n        print(f\"i={i}, j={j}\")\n```\n\nTotal iterations equal the product of both loops: `2 * 3 = 6` total steps.",
        "explanation": "Inner loops run to completion for every single step of their enclosing outer loop.",
        "metadata": {"concept": "nested_loop_execution_order", "skill": "recognition", "why_this_exercise_exists": "Teaches nested loop step order"}
    },
    "6.7_q3": {
        "id": "6.7_q3",
        "type": "micro_lesson",
        "concept": "nested_loops_grid_traversal",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["6.7_q2"],
        "title": "Traversing 2D Grids and Matrices",
        "content": "Nested loops are the standard tool for processing two-dimensional data (like spreadsheets, images, or game boards):\n\n```python\ngrid = [\n    [1, 2, 3],\n    [4, 5, 6]\n]\n\nfor row in grid:\n    for val in row:\n        print(val, end=\" \")\n    print()\n```",
        "explanation": "Outer loops iterate over rows while inner loops iterate through column elements in 2D structures.",
        "metadata": {"concept": "2d_grid_processing", "skill": "recognition", "why_this_exercise_exists": "Teaches matrix iteration"}
    },

    # 7.9 Project: String Formatter
    "7.9_q1": {
        "id": "7.9_q1",
        "type": "micro_lesson",
        "concept": "project_string_formatter_overview",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Building a Real-World String Formatter",
        "content": "Raw string data from user entry, web scraping, and CSV files is often messy: inconsistent capitalization, trailing whitespace, and unformatted numbers.\n\nA string formatter pipeline systematically normalizes text:\n1. Strips extraneous whitespace (`.strip()`)\n2. Standardizes casing (`.title()`, `.lower()`)\n3. Replaces special characters (`.replace()`)\n4. Composes clean outputs with f-strings",
        "explanation": "String formatters sanitize and assemble raw text fields into polished display strings.",
        "metadata": {"concept": "string_sanitization_pipeline", "skill": "recognition", "why_this_exercise_exists": "Roadmap for string formatter project"}
    },
    "7.9_q2": {
        "id": "7.9_q2",
        "type": "micro_lesson",
        "concept": "project_string_formatter_fstrings",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["7.9_q1"],
        "title": "Precision Formatting with f-Strings",
        "content": "Python f-strings provide powerful format specifiers inside `{value:specifier}`:\n\n* `f\"{price:.2f}\"`: Formats float to 2 decimal places (`19.50`).\n* `f\"{count:03d}\"`: Zero-pads integers to width 3 (`007`).\n* `f\"{name:>15}\"`: Right-aligns text in a 15-character column.",
        "explanation": "Format specifiers provide fine-grained alignment, rounding, and padding within f-strings.",
        "metadata": {"concept": "fstring_format_specifiers", "skill": "recognition", "why_this_exercise_exists": "Teaches advanced f-string formatting"}
    },

    # 12.1 Syntax Errors vs Runtime Errors
    "12.1_q1": {
        "id": "12.1_q1",
        "type": "micro_lesson",
        "concept": "syntax_errors_vs_runtime_errors_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Syntax Errors vs Runtime Exceptions",
        "content": "Errors in Python fall into two fundamental categories:\n\n1. **Syntax Errors:** Detected by Python's parser *before* running any code. If a file has a missing colon or unmatched parenthesis, not a single line executes.\n2. **Runtime Errors (Exceptions):** Occur while the program is actively executing valid code (e.g. dividing by zero, accessing a missing key, or calling methods on `None`).",
        "explanation": "Syntax errors halt execution at parse time before line 1 runs; runtime exceptions occur during execution.",
        "metadata": {"concept": "syntax_vs_runtime_error_distinction", "skill": "recognition", "why_this_exercise_exists": "Core mental model for debugging"}
    },
    "12.1_q3": {
        "id": "12.1_q3",
        "type": "micro_lesson",
        "concept": "syntax_errors_vs_runtime_errors_traceback",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["12.1_q2"],
        "title": "Anatomy of a Traceback",
        "content": "When a runtime exception occurs, Python prints a **traceback**.\n\nTo diagnose an error quickly, read from the bottom up:\n1. **Bottom Line:** The exception type and error message (e.g. `ValueError: invalid literal for int()`).\n2. **Line Above:** The exact file name and line number that failed.\n3. **Call Stack:** The chain of function calls leading up to the crash.",
        "explanation": "Tracebacks display the failure chain; reading the bottom line reveals the exception type and root cause.",
        "metadata": {"concept": "traceback_anatomy", "skill": "recognition", "why_this_exercise_exists": "Teaches how to read Python tracebacks"}
    },

    # 13.1 Reading Text Files
    "13.1_q1": {
        "id": "13.1_q1",
        "type": "micro_lesson",
        "concept": "reading_text_files_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Safe File I/O with with open()",
        "content": "Always open files using the `with` statement (a context manager):\n\n```python\nwith open(\"data.txt\", \"r\") as file:\n    content = file.read()\n```\n\nThe context manager guarantees that Python automatically closes the file descriptor when the block exits, even if an exception is raised inside.",
        "explanation": "with open() ensures automatic file closure, preventing operating system resource leaks.",
        "metadata": {"concept": "context_manager_file_io", "skill": "recognition", "why_this_exercise_exists": "Safe file handling fundamentals"}
    },
    "13.1_q3": {
        "id": "13.1_q3",
        "type": "micro_lesson",
        "concept": "reading_text_files_line_by_line",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["13.1_q2"],
        "title": "Memory-Efficient Line Iteration",
        "content": "For large files, avoid `file.read()` which loads the entire file into memory at once. Instead, iterate over the open file object line by line:\n\n```python\nwith open(\"large_log.txt\") as f:\n    for line in f:\n        print(line.strip())\n```\n\nThis streams lines lazily, consuming O(1) constant memory regardless of file size.",
        "explanation": "Iterating over file handles reads one line at a time, avoiding memory exhaustion on large files.",
        "metadata": {"concept": "lazy_file_streaming", "skill": "recognition", "why_this_exercise_exists": "Teaches memory-efficient file iteration"}
    },

    # 14.5 Generating JSON
    "14.5_q1": {
        "id": "14.5_q1",
        "type": "micro_lesson",
        "concept": "generating_json_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Python Objects vs JSON Strings",
        "content": "JSON (JavaScript Object Notation) is a language-independent text format for data exchange.\n\nPython maps data structures to JSON equivalents:\n* `dict` -> JSON object `{}`\n* `list` / `tuple` -> JSON array `[]`\n* `True` / `False` -> JSON booleans `true` / `false`\n* `None` -> JSON `null`\n\n`json.dumps(obj)` serializes a Python object into a JSON-formatted string.",
        "explanation": "json.dumps() converts Python dictionaries and primitives into standard JSON string representations.",
        "metadata": {"concept": "json_type_mapping", "skill": "recognition", "why_this_exercise_exists": "Teaches JSON type compatibility rules"}
    },
    "14.5_q3": {
        "id": "14.5_q3",
        "type": "micro_lesson",
        "concept": "generating_json_dump_vs_dumps",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["14.5_q2"],
        "title": "json.dump() vs json.dumps()",
        "content": "Remember the distinction between the two serialization functions:\n\n* `json.dumps(obj)`: The 's' stands for **string**. Serializes and returns a Python string in RAM.\n* `json.dump(obj, file)`: Streams serialized JSON directly into a writable file stream on disk:\n\n```python\nwith open(\"data.json\", \"w\") as f:\n    json.dump(payload, f, indent=2)\n```",
        "explanation": "json.dumps returns a string; json.dump writes directly to a file stream.",
        "metadata": {"concept": "dump_vs_dumps_distinction", "skill": "recognition", "why_this_exercise_exists": "Clarifies dump vs dumps stream API"}
    },

    # 15.2 Keyword Arguments
    "15.2_q1": {
        "id": "15.2_q1",
        "type": "micro_lesson",
        "concept": "keyword_arguments_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Named Keyword Arguments",
        "content": "When calling functions, you can specify arguments by parameter name:\n\n```python\ndef setup_user(username, role=\"viewer\"):\n    return f\"{username}: {role}\"\n\n# Order-independent call:\nsetup_user(role=\"admin\", username=\"kiran\")\n```\n\nKeyword arguments clarify meaning at call sites and allow arguments to be supplied in any order.",
        "explanation": "Keyword arguments match parameter names explicitly, avoiding ordering ambiguities.",
        "metadata": {"concept": "keyword_arguments_concept", "skill": "recognition", "why_this_exercise_exists": "Teaches keyword argument clarity"}
    },
    "15.2_q3": {
        "id": "15.2_q3",
        "type": "micro_lesson",
        "concept": "keyword_arguments_kwargs_dict",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["15.2_q2"],
        "title": "Arbitrary Keyword Arguments (**kwargs)",
        "content": "Using `**kwargs` allows a function to accept any number of named arguments, which Python packs into a dictionary:\n\n```python\ndef build_profile(first, last, **details):\n    details[\"first_name\"] = first\n    details[\"last_name\"] = last\n    return details\n```",
        "explanation": "**kwargs captures unassigned keyword arguments into a standard Python dictionary.",
        "metadata": {"concept": "kwargs_dictionary_capture", "skill": "recognition", "why_this_exercise_exists": "Teaches **kwargs dictionary packing"}
    },

    # 19.5 Groups and Extraction
    "19.5_q1": {
        "id": "19.5_q1",
        "type": "micro_lesson",
        "concept": "groups_and_extraction_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Capturing Substrings with Regex Groups",
        "content": "Parentheses `(...)` in a regular expression create **capturing groups**. When a match is found, you can extract matched segments individually:\n\n```python\nimport re\nmatch = re.search(r\"(\\w+)@([\\w.]+)\", \"user@domain.com\")\nusername, domain = match.groups()\n```",
        "explanation": "Capturing groups isolate subpatterns within a matched string for easy extraction via .groups().",
        "metadata": {"concept": "regex_capturing_groups", "skill": "recognition", "why_this_exercise_exists": "Teaches regex group extraction"}
    },
    "19.5_q3": {
        "id": "19.5_q3",
        "type": "micro_lesson",
        "concept": "groups_and_extraction_named",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["19.5_q2"],
        "title": "Named Groups for Readable Code",
        "content": "Instead of remembering integer group indices, use named groups with `(?P<name>...)`:\n\n```python\npattern = r\"(?P<area>\\d{3})-(?P<number>\\d{7})\"\nmatch = re.search(pattern, \"415-5550199\")\narea = match.group(\"area\")\n```",
        "explanation": "Named groups give descriptive labels to regex capture segments, making parsers maintainable.",
        "metadata": {"concept": "named_regex_groups", "skill": "recognition", "why_this_exercise_exists": "Teaches named regex extraction"}
    },

    # 20.3 The self Keyword
    "20.3_q1": {
        "id": "20.3_q1",
        "type": "micro_lesson",
        "concept": "the_self_keyword_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "The Role of self in Python Methods",
        "content": "In Python, `self` represents the specific instance of the class upon which a method is being called.\n\n```python\nclass Dog:\n    def __init__(self, name):\n        self.name = name  # Binds name to this specific dog\n```\n\nWhen you call `d.bark()`, Python translates it to `Dog.bark(d)` behind the scenes, passing the instance automatically as `self`.",
        "explanation": "self is the explicit reference to the current instance passed to class methods.",
        "metadata": {"concept": "self_parameter_semantics", "skill": "recognition", "why_this_exercise_exists": "Teaches instance self binding"}
    },
    "20.3_q3": {
        "id": "20.3_q3",
        "type": "micro_lesson",
        "concept": "the_self_keyword_state",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["20.3_q2"],
        "title": "Instance State and Encapsulation",
        "content": "Attributes attached to `self` belong exclusively to that instance object. Two separate instances maintain completely independent state:\n\n```python\nd1 = Dog(\"Buddy\")\nd2 = Dog(\"Milo\")\nprint(d1.name, d2.name)  # Completely separate!\n```",
        "explanation": "Assigning to self.attr isolates instance state, preventing data bleeding across objects.",
        "metadata": {"concept": "instance_state_encapsulation", "skill": "recognition", "why_this_exercise_exists": "Teaches instance state isolation"}
    },

    # 21.1 Class Attributes vs Instance Attributes
    "21.1_q1": {
        "id": "21.1_q1",
        "type": "micro_lesson",
        "concept": "class_attributes_vs_instance_attributes_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Shared Class Attributes vs Unique Instance Attributes",
        "content": "Attributes in Python OOP belong to either the class or the instance:\n\n* **Class Attributes:** Defined directly in the class body. Shared by all instances (e.g. `school = 'Hogwarts'`).\n* **Instance Attributes:** Defined on `self` inside `__init__`. Unique to each individual object (e.g. `self.student_name = name`).",
        "explanation": "Class attributes are shared across all instances; instance attributes are unique to each object.",
        "metadata": {"concept": "class_vs_instance_attributes", "skill": "recognition", "why_this_exercise_exists": "Fundamental OOP attribute distinction"}
    },
    "21.1_q3": {
        "id": "21.1_q3",
        "type": "micro_lesson",
        "concept": "class_attributes_vs_instance_attributes_shadowing",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["21.1_q2"],
        "title": "Attribute Lookup Order and Shadowing",
        "content": "When you read `obj.attribute`, Python checks `obj.__dict__` first. If missing, it falls back to `type(obj).__dict__`.\n\nAssigning `obj.attribute = new_value` creates an *instance attribute* that shadows the class attribute for that specific object only, leaving other instances untouched.",
        "explanation": "Instance assignments shadow class attributes for that instance without modifying the shared class.",
        "metadata": {"concept": "attribute_shadowing_order", "skill": "recognition", "why_this_exercise_exists": "Teaches OOP attribute lookup hierarchy"}
    },

    # 26.6 Parameterized Queries and Security
    "26.6_q1": {
        "id": "26.6_q1",
        "type": "micro_lesson",
        "concept": "parameterized_queries_and_security_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "The Danger of SQL Injection",
        "content": "Never construct SQL queries by interpolating strings or using f-strings with user input:\n\n```python\n# DANGEROUS SQL INJECTION VULNERABILITY:\nquery = f\"SELECT * FROM users WHERE email = '{user_email}'\"\n```\n\nIf a malicious user submits `' OR '1'='1`, the query structure is rewritten, allowing unauthorized data leaks or destructive deletions.",
        "explanation": "String concatenation allows attacker inputs to alter SQL query syntax, causing SQL injection.",
        "metadata": {"concept": "sql_injection_threat", "skill": "recognition", "why_this_exercise_exists": "OWASP SQL injection awareness"}
    },
    "26.6_q3": {
        "id": "26.6_q3",
        "type": "micro_lesson",
        "concept": "parameterized_queries_and_security_parameterization",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["26.6_q2"],
        "title": "How Parameterized Queries Protect Applications",
        "content": "Always pass untrusted input as parameters using the database driver's placeholder:\n\n```python\ncursor.execute(\"SELECT * FROM users WHERE email = ?\", (user_email,))\n```\n\nThe database engine compiles the SQL command structure first. When input data arrives, it is treated strictly as literal values, rendering injection mathematically impossible.",
        "explanation": "Parameterized queries separate query logic from input literals, immunizing databases against injection.",
        "metadata": {"concept": "parameterized_query_defense", "skill": "recognition", "why_this_exercise_exists": "Standard secure database programming practice"}
    },

    # 29.4 Space Complexity Concepts
    "29.4_q1": {
        "id": "29.4_q1",
        "type": "micro_lesson",
        "concept": "space_complexity_concepts_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Understanding Auxiliary Space Complexity",
        "content": "Space complexity measures how much memory an algorithm requires as input size `n` grows:\n\n* **O(1) Constant Auxiliary Space:** Allocates a few scalar variables regardless of whether input has 10 or 10,000,000 items.\n* **O(n) Linear Space:** Creates a new list, dictionary, or recursive call stack proportional to input size.",
        "explanation": "Space complexity quantifies auxiliary memory overhead scaling relative to input size.",
        "metadata": {"concept": "space_complexity_fundamentals", "skill": "recognition", "why_this_exercise_exists": "Foundational space complexity definitions"}
    },
    "29.4_q3": {
        "id": "29.4_q3",
        "type": "micro_lesson",
        "concept": "space_complexity_concepts_generators",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["29.4_q2"],
        "title": "Optimizing Space with Lazy Generators",
        "content": "List comprehensions eagerly allocate memory for every element upfront (O(n) space).\n\nGenerator expressions evaluate items on-demand one by one:\n\n```python\n# O(1) space stream:\nsquares = (x * x for x in range(1_000_000))\n```\n\nGenerators allow processing datasets larger than available physical RAM.",
        "explanation": "Generators stream items lazily in O(1) space, avoiding out-of-memory crashes on big data.",
        "metadata": {"concept": "generator_space_optimization", "skill": "recognition", "why_this_exercise_exists": "Teaches memory optimization with generators"}
    },

    # 32.2 Iteration and Transformation
    "32.2_q1": {
        "id": "32.2_q1",
        "type": "micro_lesson",
        "concept": "iteration_and_transformation_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Array Transformation Patterns",
        "content": "Transforming sequences is central to algorithmic problem solving:\n\n1. **Mapping:** Apply an operation to every element (`[x * 2 for x in nums]`).\n2. **Filtering:** Select elements satisfying a condition (`[x for x in nums if x > 0]`).\n3. **Accumulation:** Compute running totals or prefix sums across the array.",
        "explanation": "Transformation pipelines map, filter, and aggregate arrays into clean output structures.",
        "metadata": {"concept": "array_transformation_taxonomy", "skill": "recognition", "why_this_exercise_exists": "Overview of array transformation patterns"}
    },
    "32.2_q3": {
        "id": "32.2_q3",
        "type": "micro_lesson",
        "concept": "iteration_and_transformation_two_pointers",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["32.2_q2"],
        "title": "In-Place Transformations with Two Pointers",
        "content": "When modifying arrays without allocating extra memory, use two pointers:\n\n```python\nleft, right = 0, len(arr) - 1\nwhile left < right:\n    arr[left], arr[right] = arr[right], arr[left]\n    left += 1\n    right -= 1\n```\n\nThis reverses an array in-place in O(n) time and O(1) auxiliary space.",
        "explanation": "Two-pointer in-place modifications eliminate auxiliary array allocations.",
        "metadata": {"concept": "two_pointer_in_place_mechanics", "skill": "recognition", "why_this_exercise_exists": "Teaches in-place two-pointer transformations"}
    },

    # 41.1 Recognizing When to Use Two Pointers
    "41.1_q1": {
        "id": "41.1_q1",
        "type": "micro_lesson",
        "concept": "recognizing_when_to_use_two_pointers_basics",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": [],
        "title": "Pattern Recognition: The Two-Pointer Technique",
        "content": "Identify two-pointer problems by looking for these clues in problem descriptions:\n\n1. The input is a **sorted array** or string.\n2. You need to find a **pair** of elements satisfying a condition (e.g. target sum).\n3. You are asked to reverse or partition an array in-place.\n\nTwo pointers convert quadratic O(n^2) nested loops into linear O(n) passes.",
        "explanation": "Sorted inputs and pairwise search constraints are classic hallmarks for two-pointer solutions.",
        "metadata": {"concept": "two_pointer_pattern_cues", "skill": "recognition", "why_this_exercise_exists": "Teaches pattern recognition for two-pointers"}
    },
    "41.1_q3": {
        "id": "41.1_q3",
        "type": "micro_lesson",
        "concept": "recognizing_when_to_use_two_pointers_convergence",
        "skill": "recognition",
        "difficulty": "easy",
        "prerequisites": ["41.1_q2"],
        "title": "Inward Convergence vs Fast/Slow Pointers",
        "content": "Two-pointer patterns follow two distinct topologies:\n\n* **Opposite Ends (Inward):** Start at index `0` and `n - 1`, moving inward toward each other (used for sorted pair sums and palindromes).\n* **Same Direction (Fast & Slow):** Both start at `0`, moving at different speeds (used for cycle detection and in-place deduplication).",
        "explanation": "Opposite-end pointers converge inward; fast/slow pointers traverse in the same direction at varying rates.",
        "metadata": {"concept": "two_pointer_topologies", "skill": "recognition", "why_this_exercise_exists": "Contrasts inward convergence with fast/slow pointers"}
    },

    # 43.5 Final Open-Ended Mastery Challenge
    "43.5_q1": {
        "id": "43.5_q1",
        "type": "micro_lesson",
        "concept": "final_open_ended_mastery_challenge_synthesis",
        "skill": "recognition",
        "difficulty": "expert",
        "prerequisites": [],
        "title": "Architectural Synthesis of Python Paradigms",
        "content": "Python mastery requires seamlessly synthesizing multiple programming paradigms:\n\n* **Functional:** Pure functions, comprehensions, closures, and generator pipelines.\n* **Object-Oriented:** Encapsulation, dunder protocols, descriptors, and composition.\n* **Defensive Engineering:** Context managers, custom exception hierarchies, and assertions.\n\nA senior developer chooses the simplest, most readable paradigm for each specific layer.",
        "explanation": "Senior Python development balances functional pipelines, OOP protocols, and defensive error design.",
        "metadata": {"concept": "multi_paradigm_synthesis", "skill": "recognition", "why_this_exercise_exists": "Capstone synthesis overview"}
    },
    "43.5_q3": {
        "id": "43.5_q3",
        "type": "micro_lesson",
        "concept": "final_open_ended_mastery_challenge_production_readiness",
        "skill": "recognition",
        "difficulty": "expert",
        "prerequisites": ["43.5_q2"],
        "title": "Production-Grade Engineering Principles",
        "content": "Before deploying Python software to production, evaluate:\n\n1. **Memory & Scaling:** Are massive files streamed lazily or loaded eagerly into RAM?\n2. **Security:** Are queries parameterized? Are inputs sanitized?\n3. **Failure Isolation:** Do worker tasks handle timeouts and exceptions without crashing the process?\n4. **Observability:** Does the system produce structured logs and telemetry metrics?",
        "explanation": "Production readiness demands lazy streaming, parameterization, fault tolerance, and observability.",
        "metadata": {"concept": "production_readiness_checklist", "skill": "recognition", "why_this_exercise_exists": "Production readiness checklist for final mastery"}
    }
}

