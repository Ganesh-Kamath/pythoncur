"""
CODOLINGO EXACT REPAIRS: SCAFFOLD FILLER PURGE
Replaces all 54 placeholder questions matching 'Complete the code to output <Title> #X'
across lessons:
4.1, 4.2, 5.2, 7.3, 11.3, 12.1, 13.4, 21.1, 24.2, 26.6, 27.2, 32.1, 33.2, 39.3
"""

REPLACEMENTS_SCAFFOLD_FILLERS = {
    # 4.1 input()
    "4.1_q13": {
        "id": "4.1_q13",
        "type": "fill_in_the_blank",
        "concept": "input_prompt_formatting",
        "skill": "syntax",
        "difficulty": "easy",
        "prerequisites": ["4.1_q12"],
        "prompt": "Fill in the blank to prompt the user with `\"Enter city: \"` and store the result in `city`:\n\n```python\ncity = ___(\"Enter city: \")\n```",
        "correct_answer": "input",
        "accepted_answers": ["input"],
        "explanation": "Passing a prompt string argument to `input(\"Enter city: \")` prints the prompt text to standard output without adding a trailing newline, keeping the user's cursor on the same line.",
        "metadata": {"concept": "input_prompt", "skill": "syntax", "why_this_exercise_exists": "Replaces filler with practical prompt syntax"}
    },
    "4.1_q14": {
        "id": "4.1_q14",
        "type": "write_the_code",
        "concept": "input_normalization_upper",
        "skill": "transformation",
        "difficulty": "medium",
        "prerequisites": ["4.1_q13"],
        "prompt": "Given `code = 'ny'`, convert the input code to uppercase `'NY'` and print `f'State: {code.upper()}'`.",
        "starter_code": "code = \"ny\"\n# Convert to uppercase and print\n",
        "solution_code": "code = \"ny\"\nstate_code = code.upper()\nprint(f\"State: {state_code}\")",
        "explanation": "Normalizing user input with `.upper()` ensures case-insensitive matching across database records and lookups.",
        "metadata": {"concept": "case_normalization", "skill": "transformation", "why_this_exercise_exists": "Replaces filler with practical input normalization"}
    },
    "4.1_q16": {
        "id": "4.1_q16",
        "type": "code_prediction",
        "concept": "input_isdigit_validation",
        "skill": "validation",
        "difficulty": "medium",
        "prerequisites": ["4.1_q15"],
        "prompt": "What does `\"42\".isdigit()` return when validating user input?",
        "options": ["True", "False", "TypeError", "42"],
        "correct_answer": "True",
        "explanation": "`.isdigit()` checks if all characters in the string are digits (0-9). For `\"42\"`, it returns `True`, making it an effective pre-check before calling `int()`.",
        "metadata": {"concept": "input_digit_validation", "skill": "validation", "why_this_exercise_exists": "Replaces filler with input validation"}
    },
    "4.1_q18": {
        "id": "4.1_q18",
        "type": "fix_the_code",
        "concept": "input_cleaning_strip",
        "skill": "sanitization",
        "difficulty": "medium",
        "prerequisites": ["4.1_q17"],
        "prompt": "Fix the line below to strip surrounding quotation marks from user input `raw_tag = '\"science\"'`:\n\n```python\nraw_tag = '\"science\"'\n# Fix using strip:\nclean_tag = raw_tag.strip('\"')\nprint(clean_tag)\n```",
        "starter_code": "raw_tag = '\"science\"'\nclean_tag = raw_tag.strip('\"')\nprint(clean_tag)",
        "solution_code": "raw_tag = '\"science\"'\nclean_tag = raw_tag.strip('\"')\nprint(clean_tag)",
        "explanation": "Passing characters to `.strip('\"')` instructs Python to strip double quote characters from the start and end of the string, yielding `'science'`.",
        "metadata": {"concept": "custom_character_stripping", "skill": "sanitization", "why_this_exercise_exists": "Replaces filler with custom stripping"}
    },

    # 4.2 Numeric Input
    "4.2_q13": {
        "id": "4.2_q13",
        "type": "write_the_code",
        "concept": "numeric_input_multiplication",
        "skill": "arithmetic",
        "difficulty": "medium",
        "prerequisites": ["4.2_q12"],
        "prompt": "Given a quantity string `qty_str = '5'`, parse it as an integer, multiply by price `10`, and store in `total`.",
        "starter_code": "qty_str = \"5\"\nprice = 10\n# Convert and compute total\n",
        "solution_code": "qty_str = \"5\"\nprice = 10\ntotal = int(qty_str) * price\nprint(total)",
        "explanation": "Converting `qty_str` with `int()` allows integer multiplication `5 * 10 = 50`.",
        "metadata": {"concept": "int_multiplication", "skill": "implementation", "why_this_exercise_exists": "Replaces filler with numeric input math"}
    },
    "4.2_q14": {
        "id": "4.2_q14",
        "type": "fix_the_code",
        "concept": "numeric_input_percentage",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["4.2_q13"],
        "prompt": "A user enters a percentage as `'15%'`. Fix the code so it strips the `'%'` character before converting to float `0.15`:\n\n```python\nrate_str = \"15%\"\n# Fix conversion:\nrate = float(rate_str.rstrip(\"%\")) / 100\nprint(rate)\n```",
        "starter_code": "rate_str = \"15%\"\nrate = float(rate_str.rstrip(\"%\")) / 100\nprint(rate)",
        "solution_code": "rate_str = \"15%\"\nrate = float(rate_str.rstrip(\"%\")) / 100\nprint(rate)",
        "explanation": "Calling `.rstrip('%')` removes the trailing percent sign, leaving `'15'`, which converts cleanly to float `15.0 / 100 = 0.15`.",
        "metadata": {"concept": "percentage_string_parsing", "skill": "repair", "why_this_exercise_exists": "Replaces filler with percentage parsing"}
    },
    "4.2_q16": {
        "id": "4.2_q16",
        "type": "error_diagnosis",
        "concept": "numeric_input_try_except",
        "skill": "defensive_programming",
        "difficulty": "medium",
        "prerequisites": ["4.2_q15"],
        "prompt": "What exception must you catch when calling `int(text)` on untrusted user text?",
        "options": [
            "ValueError",
            "TypeError",
            "IndexError",
            "KeyError"
        ],
        "correct_answer": "ValueError",
        "explanation": "If `text` contains non-digit characters (like `'abc'`), `int()` raises `ValueError: invalid literal for int()`. Wrapping in `try: ... except ValueError:` prevents program crashes.",
        "metadata": {"concept": "value_error_handling", "skill": "error_recognition", "why_this_exercise_exists": "Replaces filler with exception handling"}
    },
    "4.2_q18": {
        "id": "4.2_q18",
        "type": "write_the_code",
        "concept": "numeric_input_safe_parser",
        "skill": "robust_parsing",
        "difficulty": "hard",
        "prerequisites": ["4.2_q17"],
        "prompt": "Write a safe parsing function `parse_int_safe(text, default=0)` that returns `int(text)` if valid, or `default` if conversion raises ValueError.",
        "starter_code": "def parse_int_safe(text, default=0):\n    # Return parsed int or default\n    pass",
        "solution_code": "def parse_int_safe(text, default=0):\n    try:\n        return int(text)\n    except (ValueError, TypeError):\n        return default\n\nprint(parse_int_safe(\"100\"), parse_int_safe(\"bad\", -1))",
        "explanation": "Catching `(ValueError, TypeError)` handles both non-numeric strings and `None` gracefully, returning the designated fallback.",
        "metadata": {"concept": "safe_numeric_fallback", "skill": "implementation", "why_this_exercise_exists": "Replaces filler with production input parser"}
    },

    # 5.2 else
    "5.2_q16": {
        "id": "5.2_q16",
        "type": "code_prediction",
        "concept": "else_even_odd",
        "skill": "branch_tracing",
        "difficulty": "easy",
        "prerequisites": ["5.2_q15"],
        "prompt": "What does this code print for `n = 7`?\n\n```python\nn = 7\nif n % 2 == 0:\n    print(\"Even\")\nelse:\n    print(\"Odd\")\n```",
        "options": ["Odd", "Even", "0", "1"],
        "correct_answer": "Odd",
        "explanation": "`7 % 2` evaluates to 1, so `1 == 0` is `False`. The `else` branch executes, printing `'Odd'`.",
        "metadata": {"concept": "parity_branching", "skill": "tracing", "why_this_exercise_exists": "Replaces filler with classic even/odd branching"}
    },
    "5.2_q18": {
        "id": "5.2_q18",
        "type": "write_the_code",
        "concept": "else_pass_fail",
        "skill": "construction",
        "difficulty": "medium",
        "prerequisites": ["5.2_q17"],
        "prompt": "Write an `if-else` statement that sets `status = 'Pass'` if `score >= 50`, else `status = 'Fail'`. Test with `score = 48`.",
        "starter_code": "score = 48\n# Write if-else below:\n",
        "solution_code": "score = 48\nif score >= 50:\n    status = \"Pass\"\nelse:\n    status = \"Fail\"\nprint(status)",
        "explanation": "Because `48 >= 50` is `False`, the `else` branch sets `status = 'Fail'`.",
        "metadata": {"concept": "pass_fail_evaluation", "skill": "construction", "why_this_exercise_exists": "Replaces filler with threshold categorization"}
    },

    # 7.3 String Slicing
    "7.3_q13": {
        "id": "7.3_q13",
        "type": "code_prediction",
        "concept": "string_slicing_prefix",
        "skill": "slicing",
        "difficulty": "easy",
        "prerequisites": ["7.3_q12"],
        "prompt": "What does `text[:3]` extract from `text = 'Python'`?",
        "options": ["Pyt", "Pyth", "yth", "on"],
        "correct_answer": "Pyt",
        "explanation": "`[:3]` extracts characters from index 0 up to (but not including) index 3: indices 0 ('P'), 1 ('y'), and 2 ('t') -> `'Pyt'`.",
        "metadata": {"concept": "prefix_slice", "skill": "slicing", "why_this_exercise_exists": "Replaces filler with string prefix slicing"}
    },
    "7.3_q14": {
        "id": "7.3_q14",
        "type": "code_prediction",
        "concept": "string_slicing_suffix",
        "skill": "negative_indexing",
        "difficulty": "medium",
        "prerequisites": ["7.3_q13"],
        "prompt": "What does `filename[-4:]` return for `filename = 'document.pdf'`?",
        "options": [".pdf", "pdf", "t.pdf", "docu"],
        "correct_answer": ".pdf",
        "explanation": "Negative start index `-4` starts 4 characters from the end through to the string terminus, returning `'.pdf'`.",
        "metadata": {"concept": "suffix_slice", "skill": "negative_indexing", "why_this_exercise_exists": "Replaces filler with extension extraction"}
    },
    "7.3_q16": {
        "id": "7.3_q16",
        "type": "code_prediction",
        "concept": "string_slicing_step_reverse",
        "skill": "step_slicing",
        "difficulty": "medium",
        "prerequisites": ["7.3_q15"],
        "prompt": "What does `word[::-1]` do to `word = 'live'`?",
        "options": ["evil", "live", "veil", "None"],
        "correct_answer": "evil",
        "explanation": "A step of `-1` strides backward from the end to the beginning, reversing the string: `'live'` -> `'evil'`.",
        "metadata": {"concept": "string_reversal_slice", "skill": "step_slicing", "why_this_exercise_exists": "Replaces filler with reversal slice"}
    },
    "7.3_q18": {
        "id": "7.3_q18",
        "type": "write_the_code",
        "concept": "string_slicing_domain_extract",
        "skill": "slicing_application",
        "difficulty": "hard",
        "prerequisites": ["7.3_q17"],
        "prompt": "Given `email = 'ada@lovelace.org'`, find the index of `'@'` and slice out only the domain name `'lovelace.org'` into variable `domain`.",
        "starter_code": "email = \"ada@lovelace.org\"\n# Slice out domain\n",
        "solution_code": "email = \"ada@lovelace.org\"\nat_idx = email.index(\"@\")\ndomain = email[at_idx + 1:]\nprint(domain)",
        "explanation": "Finding `@` at index 3, slicing from `at_idx + 1` (index 4) to the end extracts `'lovelace.org'`.",
        "metadata": {"concept": "dynamic_slice_extraction", "skill": "implementation", "why_this_exercise_exists": "Replaces filler with email domain slicing"}
    },

    # 11.3 Parameters and Arguments
    "11.3_q13": {
        "id": "11.3_q13",
        "type": "write_the_code",
        "concept": "parameters_default_greeting",
        "skill": "function_design",
        "difficulty": "medium",
        "prerequisites": ["11.3_q12"],
        "prompt": "Define a function `greet(name, greeting='Hello')` that returns `f'{greeting}, {name}!'`. Call it with `name='Maya'` without passing greeting.",
        "starter_code": "def greet(name, greeting=\"Hello\"):\n    pass\n\nmsg = greet(\"Maya\")\nprint(msg)",
        "solution_code": "def greet(name, greeting=\"Hello\"):\n    return f\"{greeting}, {name}!\"\n\nmsg = greet(\"Maya\")\nprint(msg)",
        "explanation": "When `greeting` is omitted, it takes default value `'Hello'`, producing `'Hello, Maya!'`.",
        "metadata": {"concept": "default_parameter_usage", "skill": "function_design", "why_this_exercise_exists": "Replaces filler with default parameter greeting"}
    },
    "11.3_q14": {
        "id": "11.3_q14",
        "type": "output_prediction",
        "concept": "keyword_argument_clarity",
        "skill": "tracing",
        "difficulty": "medium",
        "prerequisites": ["11.3_q13"],
        "prompt": "What does calling `describe_pet(pet_name=\"Whiskers\", animal_type=\"cat\")` return?\n\n```python\ndef describe_pet(animal_type, pet_name):\n    return f\"{pet_name} is a {animal_type}\"\n\nprint(describe_pet(pet_name=\"Whiskers\", animal_type=\"cat\"))\n```",
        "options": ["Whiskers is a cat", "cat is a Whiskers", "TypeError", "None"],
        "correct_answer": "Whiskers is a cat",
        "explanation": "Keyword arguments match parameter names explicitly, avoiding positional ordering errors.",
        "metadata": {"concept": "named_argument_order", "skill": "tracing", "why_this_exercise_exists": "Replaces filler with keyword argument invocation"}
    },
    "11.3_q16": {
        "id": "11.3_q16",
        "type": "error_diagnosis",
        "concept": "duplicate_argument_error",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["11.3_q15"],
        "prompt": "Why does calling `greet(\"Aria\", name=\"Maya\")` raise a TypeError?\n\n```python\ndef greet(name):\n    return f\"Hello {name}\"\n\ngreet(\"Aria\", name=\"Maya\")\n```",
        "options": [
            "TypeError: greet() got multiple values for argument 'name'",
            "SyntaxError: invalid argument combination",
            "NameError: Aria is not defined",
            "ValueError: duplicate name detected"
        ],
        "correct_answer": "TypeError: greet() got multiple values for argument 'name'",
        "explanation": "`\"Aria\"` was passed positionally for `name`, and then `name=\"Maya\"` attempted to bind the same parameter a second time, which Python forbids.",
        "metadata": {"concept": "duplicate_parameter_binding", "skill": "debugging", "why_this_exercise_exists": "Replaces filler with parameter collision debugging"}
    },
    "11.3_q18": {
        "id": "11.3_q18",
        "type": "write_the_code",
        "concept": "arbitrary_positional_args",
        "skill": "implementation",
        "difficulty": "hard",
        "prerequisites": ["11.3_q17"],
        "prompt": "Write a function `sum_all(*numbers)` that sums any quantity of numeric arguments passed to it. Call it with `1, 2, 3, 4`.",
        "starter_code": "def sum_all(*numbers):\n    # Return sum of all numbers\n    pass",
        "solution_code": "def sum_all(*numbers):\n    return sum(numbers)\n\nprint(sum_all(1, 2, 3, 4))",
        "explanation": "`*numbers` packs incoming positional arguments into a tuple `(1, 2, 3, 4)`, which `sum()` aggregates to `10`.",
        "metadata": {"concept": "varargs_star_args", "skill": "implementation", "why_this_exercise_exists": "Replaces filler with *args implementation"}
    },

    # 12.1 Syntax Errors vs Runtime Errors
    "12.1_q13": {
        "id": "12.1_q13",
        "type": "error_diagnosis",
        "concept": "unclosed_parenthesis_syntax_error",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["12.1_q12"],
        "prompt": "What error occurs if you forget to close a parenthesis: `total = (10 + 20`?",
        "options": [
            "SyntaxError: '(' was never closed",
            "RuntimeError: incomplete evaluation",
            "TypeError: missing closing token",
            "ValueError: unclosed expression"
        ],
        "correct_answer": "SyntaxError: '(' was never closed",
        "explanation": "Modern Python 3.10+ parsers explicitly report `SyntaxError: '(' was never closed` pointing directly to the unclosed bracket.",
        "metadata": {"concept": "unclosed_delimiter_syntax", "skill": "debugging", "why_this_exercise_exists": "Replaces filler with compiler error diagnostics"}
    },
    "12.1_q14": {
        "id": "12.1_q14",
        "type": "error_diagnosis",
        "concept": "zerodivision_runtime_error",
        "skill": "error_discrimination",
        "difficulty": "medium",
        "prerequisites": ["12.1_q13"],
        "prompt": "Is `result = 10 / 0` a SyntaxError or a RuntimeError?",
        "options": [
            "RuntimeError (specifically ZeroDivisionError), because the syntax is grammatically valid and fails only during execution.",
            "SyntaxError, because dividing by zero is forbidden by Python's grammar.",
            "NameError, because zero is undefined.",
            "TypeError, because 0 cannot be an operand."
        ],
        "correct_answer": "RuntimeError (specifically ZeroDivisionError), because the syntax is grammatically valid and fails only during execution.",
        "explanation": "Grammatically, `10 / 0` is valid Python. The error only manifests at runtime when the CPU executes the division instruction.",
        "metadata": {"concept": "runtime_vs_syntax_classification", "skill": "discrimination", "why_this_exercise_exists": "Replaces filler with core error category distinction"}
    },
    "12.1_q16": {
        "id": "12.1_q16",
        "type": "fix_the_code",
        "concept": "name_error_typo_fix",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["12.1_q15"],
        "prompt": "Fix the NameError typo in this calculation:\n\n```python\nsubtotal = 50.0\n# Fix typo in variable name:\ntotal = subtotl * 1.1\nprint(total)\n```",
        "starter_code": "subtotal = 50.0\ntotal = subtotl * 1.1\nprint(total)",
        "solution_code": "subtotal = 50.0\ntotal = subtotal * 1.1\nprint(total)",
        "explanation": "Correcting the typo `subtotl` to `subtotal` resolves the runtime NameError.",
        "metadata": {"concept": "name_error_typo", "skill": "repair", "why_this_exercise_exists": "Replaces filler with real variable typo repair"}
    },
    "12.1_q18": {
        "id": "12.1_q18",
        "type": "multiple_choice",
        "concept": "logic_error_definition",
        "skill": "classification",
        "difficulty": "medium",
        "prerequisites": ["12.1_q17"],
        "prompt": "What defines a 'Logic Error' (semantic error) in Python?",
        "options": [
            "The program compiles and runs to completion without raising an exception, but produces incorrect output.",
            "An error that stops Python from compiling the file.",
            "An error that triggers a traceback immediately.",
            "An error caused by insufficient RAM."
        ],
        "correct_answer": "The program compiles and runs to completion without raising an exception, but produces incorrect output.",
        "explanation": "Logic errors are the most insidious bugs because Python does not crash; the algorithm simply produces flawed business results (e.g. calculating `price + discount` instead of `price - discount`).",
        "metadata": {"concept": "logic_error_nature", "skill": "classification", "why_this_exercise_exists": "Replaces filler with logic error awareness"}
    },

    # 13.4 Writing to Files
    "13.4_q13": {
        "id": "13.4_q13",
        "type": "code_prediction",
        "concept": "file_write_mode_w_destructive",
        "skill": "file_io",
        "difficulty": "medium",
        "prerequisites": ["13.4_q12"],
        "prompt": "What happens if you open an existing file in `'w'` mode and write `'New content'`?",
        "options": [
            "The entire previous content is immediately truncated (erased) and overwritten.",
            "The text is appended to the bottom.",
            "An error is raised if the file already exists.",
            "A second copy of the file is created."
        ],
        "correct_answer": "The entire previous content is immediately truncated (erased) and overwritten.",
        "explanation": "Write mode `'w'` truncates existing files to 0 bytes upon opening. To preserve existing data and add to the bottom, mode `'a'` (append) must be used.",
        "metadata": {"concept": "write_mode_truncation", "skill": "file_io", "why_this_exercise_exists": "Replaces filler with destructive write warning"}
    },
    "13.4_q14": {
        "id": "13.4_q14",
        "type": "write_the_code",
        "concept": "file_append_mode_usage",
        "skill": "implementation",
        "difficulty": "medium",
        "prerequisites": ["13.4_q13"],
        "prompt": "Write a snippet using `with open('log.txt', 'a') as f:` that appends a log entry `'System OK\\n'` to the file.",
        "starter_code": "# Append to log.txt\n",
        "solution_code": "with open(\"log.txt\", \"a\") as f:\n    f.write(\"System OK\\n\")",
        "explanation": "Mode `'a'` opens the file with the write pointer positioned at the end of the file, preserving existing records and appending new lines.",
        "metadata": {"concept": "file_append_mode", "skill": "implementation", "why_this_exercise_exists": "Replaces filler with log appending"}
    },
    "13.4_q16": {
        "id": "13.4_q16",
        "type": "error_diagnosis",
        "concept": "file_exclusive_creation_mode_x",
        "skill": "file_modes",
        "difficulty": "medium",
        "prerequisites": ["13.4_q15"],
        "prompt": "What does mode `'x'` do when opening a file that already exists on disk?",
        "options": [
            "Raises FileExistsError: [Errno 17] File exists",
            "Overwrites the file silently",
            "Appends to the file",
            "Renames the old file"
        ],
        "correct_answer": "Raises FileExistsError: [Errno 17] File exists",
        "explanation": "Mode `'x'` provides exclusive creation. It opens the file for writing only if it does not already exist, raising `FileExistsError` if the file is present to prevent accidental data overwrites.",
        "metadata": {"concept": "exclusive_file_creation", "skill": "file_modes", "why_this_exercise_exists": "Replaces filler with exclusive mode protection"}
    },
    "13.4_q18": {
        "id": "13.4_q18",
        "type": "write_the_code",
        "concept": "writelines_list_writing",
        "skill": "implementation",
        "difficulty": "hard",
        "prerequisites": ["13.4_q17"],
        "prompt": "Given `lines = ['Alpha\\n', 'Beta\\n', 'Gamma\\n']`, write all lines to `'output.txt'` using `f.writelines(lines)` within a `with` block.",
        "starter_code": "lines = [\"Alpha\\n\", \"Beta\\n\", \"Gamma\\n\"]\n# Write lines using writelines\n",
        "solution_code": "lines = [\"Alpha\\n\", \"Beta\\n\", \"Gamma\\n\"]\nwith open(\"output.txt\", \"w\") as f:\n    f.writelines(lines)",
        "explanation": "`f.writelines(lines)` efficiently writes an iterable of strings to the stream in a single call.",
        "metadata": {"concept": "writelines_bulk_io", "skill": "implementation", "why_this_exercise_exists": "Replaces filler with writelines bulk writing"}
    },

    # 21.1 Class Attributes vs Instance Attributes
    "21.1_q13": {
        "id": "21.1_q13",
        "type": "write_the_code",
        "concept": "instance_counter_class_attr",
        "skill": "oop_design",
        "difficulty": "medium",
        "prerequisites": ["21.1_q12"],
        "prompt": "Create a class `User` with class attribute `total_users = 0`. In `__init__`, increment `User.total_users += 1` on each instance creation. Test by instantiating two users.",
        "starter_code": "class User:\n    total_users = 0\n    def __init__(self, username):\n        self.username = username\n        # Increment User.total_users\n        pass",
        "solution_code": "class User:\n    total_users = 0\n    def __init__(self, username):\n        self.username = username\n        User.total_users += 1\n\nu1 = User(\"Alice\")\nu2 = User(\"Bob\")\nprint(User.total_users)",
        "explanation": "Referencing `User.total_users += 1` directly on the class modifies the shared class attribute, successfully tracking total instances created.",
        "metadata": {"concept": "instance_tracking_class_attribute", "skill": "oop_design", "why_this_exercise_exists": "Replaces filler with instance counter pattern"}
    },
    "21.1_q14": {
        "id": "21.1_q14",
        "type": "code_prediction",
        "concept": "class_attr_introspection",
        "skill": "introspection",
        "difficulty": "medium",
        "prerequisites": ["21.1_q13"],
        "prompt": "Where are class attributes stored in Python's object model?",
        "options": [
            "In the class's __dict__ namespace dictionary.",
            "In the instance's __dict__ on every object.",
            "In the global sys module.",
            "In Python bytecode constants."
        ],
        "correct_answer": "In the class's __dict__ namespace dictionary.",
        "explanation": "Class attributes live in `ClassName.__dict__`. When an attribute is looked up on an instance `obj.attr`, Python first checks `obj.__dict__`; if not found, it checks `type(obj).__dict__`.",
        "metadata": {"concept": "class_dict_namespace", "skill": "introspection", "why_this_exercise_exists": "Replaces filler with OOP namespace model"}
    },
    "21.1_q16": {
        "id": "21.1_q16",
        "type": "output_prediction",
        "concept": "class_attribute_override_instance",
        "skill": "attribute_resolution",
        "difficulty": "medium",
        "prerequisites": ["21.1_q15"],
        "prompt": "What does `e1.department` print after modifying `e1.department`?\n\n```python\nclass Employee:\n    department = \"Engineering\"\n\ne1 = Employee()\ne2 = Employee()\ne1.department = \"Design\"\nprint(e1.department, e2.department)\n```",
        "options": [
            "Design Engineering",
            "Design Design",
            "Engineering Engineering",
            "AttributeError"
        ],
        "correct_answer": "Design Engineering",
        "explanation": "`e1.department = 'Design'` assigns an instance attribute to `e1`. `e2` does not have an instance attribute, so it resolves to the shared class attribute `'Engineering'`.",
        "metadata": {"concept": "instance_shadowing_isolation", "skill": "attribute_resolution", "why_this_exercise_exists": "Replaces filler with attribute shadowing"}
    },
    "21.1_q18": {
        "id": "21.1_q18",
        "type": "fix_the_code",
        "concept": "class_attr_mutation_cleanup",
        "skill": "repair",
        "difficulty": "hard",
        "prerequisites": ["21.1_q17"],
        "prompt": "Fix this class so `tags` is initialized as a fresh empty set for each instance rather than shared at class level:\n\n```python\nclass Article:\n    tags = set()  # Bug: shared across all articles\n    def __init__(self, title):\n        self.title = title\n```",
        "starter_code": "class Article:\n    tags = set()\n    def __init__(self, title):\n        self.title = title",
        "solution_code": "class Article:\n    def __init__(self, title):\n        self.title = title\n        self.tags = set()",
        "explanation": "Moving `self.tags = set()` into `__init__` ensures every article gets its own independent set.",
        "metadata": {"concept": "mutable_instance_isolation", "skill": "repair", "why_this_exercise_exists": "Replaces filler with mutable attribute bug fix"}
    },

    # 24.2 Docstrings
    "24.2_q13": {
        "id": "24.2_q13",
        "type": "write_the_code",
        "concept": "docstring_one_liner",
        "skill": "documentation",
        "difficulty": "easy",
        "prerequisites": ["24.2_q12"],
        "prompt": "Add a proper PEP 257 one-line docstring to this function: `\"\"\"Return the absolute value of number.\"\"\"`.",
        "starter_code": "def get_abs(num):\n    # Add docstring here\n    return abs(num)",
        "solution_code": "def get_abs(num):\n    \"\"\"Return the absolute value of number.\"\"\"\n    return abs(num)",
        "explanation": "A one-line docstring begins and ends with triple quotes on the same line, describing the function's effect as an imperative command.",
        "metadata": {"concept": "pep257_one_liner", "skill": "documentation", "why_this_exercise_exists": "Replaces filler with one-line docstring format"}
    },
    "24.2_q14": {
        "id": "24.2_q14",
        "type": "code_prediction",
        "concept": "docstring_multiline_structure",
        "skill": "documentation",
        "difficulty": "medium",
        "prerequisites": ["24.2_q13"],
        "prompt": "In a multi-line docstring according to PEP 257, what should immediately follow the first summary line?",
        "options": [
            "A blank line separating the summary from the detailed description.",
            "The closing triple quotes immediately.",
            "The author's email address.",
            "A list of import statements."
        ],
        "correct_answer": "A blank line separating the summary from the detailed description.",
        "explanation": "PEP 257 specifies: summary line, followed by a blank line, followed by the elaborated description and parameter documentation.",
        "metadata": {"concept": "pep257_multiline_format", "skill": "documentation", "why_this_exercise_exists": "Replaces filler with docstring structure rules"}
    },
    "24.2_q16": {
        "id": "24.2_q16",
        "type": "write_the_code",
        "concept": "docstring_returns_documentation",
        "skill": "documentation",
        "difficulty": "medium",
        "prerequisites": ["24.2_q15"],
        "prompt": "Write a function `is_valid_email(email)` with a docstring that documents the boolean return value: `Returns: True if valid, False otherwise.`.",
        "starter_code": "def is_valid_email(email):\n    # Document return contract\n    pass",
        "solution_code": "def is_valid_email(email):\n    \"\"\"Validate email syntax.\n\n    Returns:\n        bool: True if valid, False otherwise.\n    \"\"\"\n    return \"@\" in email and \".\" in email",
        "explanation": "Explicitly documenting return semantics allows users and automated linters to understand the function's contract without reading its body.",
        "metadata": {"concept": "return_contract_documentation", "skill": "documentation", "why_this_exercise_exists": "Replaces filler with return docstring formatting"}
    },
    "24.2_q18": {
        "id": "24.2_q18",
        "type": "output_prediction",
        "concept": "docstring_none_when_omitted",
        "skill": "introspection",
        "difficulty": "medium",
        "prerequisites": ["24.2_q17"],
        "prompt": "What is `func.__doc__` if a function has no docstring defined?\n\n```python\ndef no_docs():\n    pass\n\nprint(no_docs.__doc__)\n```",
        "options": ["None", "\"\"", "AttributeError", "no_docs"],
        "correct_answer": "None",
        "explanation": "If no docstring is present, Python assigns `None` to the function's `__doc__` attribute.",
        "metadata": {"concept": "docstring_default_none", "skill": "introspection", "why_this_exercise_exists": "Replaces filler with docstring runtime reflection"}
    },

    # 26.6 Parameterized Queries
    "26.6_q13": {
        "id": "26.6_q13",
        "type": "write_the_code",
        "concept": "parameterized_select_query",
        "skill": "database_security",
        "difficulty": "medium",
        "prerequisites": ["26.6_q12"],
        "prompt": "Write a safe parameterized SELECT statement to fetch a user by email `'ada@lovelace.org'` using `cursor.execute('SELECT * FROM users WHERE email = ?', (email,))`.",
        "starter_code": "email = \"ada@lovelace.org\"\n# Execute safe parameterized query\n",
        "solution_code": "email = \"ada@lovelace.org\"\n# In production: cursor.execute(\"SELECT * FROM users WHERE email = ?\", (email,))\nquery = \"SELECT * FROM users WHERE email = ?\"\nparams = (email,)\nprint(f\"Safe query: {query} with {params}\")",
        "explanation": "Parameterized queries separate SQL instructions from user inputs, preventing SQL injection.",
        "metadata": {"concept": "parameterized_select", "skill": "security", "why_this_exercise_exists": "Replaces filler with secure query design"}
    },
    "26.6_q14": {
        "id": "26.6_q14",
        "type": "write_the_code",
        "concept": "parameterized_insert_query",
        "skill": "database_security",
        "difficulty": "medium",
        "prerequisites": ["26.6_q13"],
        "prompt": "Write a parameterized INSERT statement with two placeholders `?` to insert a product `name = 'Keyboard'` and `price = 49.99` into table `products`.",
        "starter_code": "name = \"Keyboard\"\nprice = 49.99\n# Build parameterized insert\n",
        "solution_code": "name = \"Keyboard\"\nprice = 49.99\nquery = \"INSERT INTO products (name, price) VALUES (?, ?)\"\nparams = (name, price)\nprint(f\"Insert: {query} with {params}\")",
        "explanation": "Using multiple `?` placeholders binds multi-column records safely without manual quotation.",
        "metadata": {"concept": "parameterized_insert", "skill": "security", "why_this_exercise_exists": "Replaces filler with parameterized INSERT"}
    },
    "26.6_q16": {
        "id": "26.6_q16",
        "type": "code_prediction",
        "concept": "named_sql_parameters",
        "skill": "database_patterns",
        "difficulty": "medium",
        "prerequisites": ["26.6_q15"],
        "prompt": "In Python's `sqlite3`, what dictionary-style parameter placeholder format is supported alongside `?`?",
        "options": [
            "Named placeholders with colons (e.g. :name and :price) passed via a dictionary.",
            "Brackets with numbers [0] and [1].",
            "Dollar signs ($name, $price).",
            "Percentage signs (%1, %2)."
        ],
        "correct_answer": "Named placeholders with colons (e.g. :name and :price) passed via a dictionary.",
        "explanation": "`sqlite3` supports named placeholders `:col` when arguments are passed in a dictionary `{'col': value}`.",
        "metadata": {"concept": "named_sql_placeholders", "skill": "database_patterns", "why_this_exercise_exists": "Replaces filler with named query placeholders"}
    },
    "26.6_q18": {
        "id": "26.6_q18",
        "type": "multiple_choice",
        "concept": "table_name_parameterization_limit",
        "skill": "security_architecture",
        "difficulty": "hard",
        "prerequisites": ["26.6_q17"],
        "prompt": "Can table or column names be parameterized using `?` in SQL?",
        "options": [
            "No; SQL drivers only permit parameters for literal data values. Table/column names must be validated against a strict allowlist in Python.",
            "Yes; cursor.execute('SELECT * FROM ?', (table_name,)) works standardly.",
            "Yes; table names are encrypted by the database driver.",
            "No; table names must always be prompted via input()."
        ],
        "correct_answer": "No; SQL drivers only permit parameters for literal data values. Table/column names must be validated against a strict allowlist in Python.",
        "explanation": "SQL parameters only replace literal values. Passing a table or column name as `?` causes a syntax error. Dynamic table names must be strictly validated against an approved Python whitelist before insertion.",
        "metadata": {"concept": "dynamic_table_whitelist_defense", "skill": "security_architecture", "why_this_exercise_exists": "Replaces filler with subtle SQL driver limitation rule"}
    },

    # 27.2 Defining Routes
    "27.2_q13": {
        "id": "27.2_q13",
        "type": "code_prediction",
        "concept": "route_path_parameters",
        "skill": "api_routing",
        "difficulty": "medium",
        "prerequisites": ["27.2_q12"],
        "prompt": "In FastAPI or Flask, how is a dynamic path parameter defined in the route decorator?",
        "options": [
            "@app.get('/users/{user_id}') in FastAPI (or '/users/<int:user_id>' in Flask)",
            "@app.get('/users/user_id?')",
            "@app.get('/users/$user_id')",
            "@app.get('/users/regex')"
        ],
        "correct_answer": "@app.get('/users/{user_id}') in FastAPI (or '/users/<int:user_id>' in Flask)",
        "explanation": "FastAPI uses `{param}` brackets with type hints; Flask uses `<converter:param>` tags.",
        "metadata": {"concept": "path_parameter_syntax", "skill": "routing", "why_this_exercise_exists": "Replaces filler with path parameter syntax"}
    },
    "27.2_q14": {
        "id": "27.2_q14",
        "type": "write_the_code",
        "concept": "json_endpoint_response",
        "skill": "api_design",
        "difficulty": "medium",
        "prerequisites": ["27.2_q13"],
        "prompt": "Write a route handler function `get_status()` that returns a dictionary `{'status': 'ok', 'version': '1.0'}`.",
        "starter_code": "def get_status():\n    # Return JSON dictionary\n    pass",
        "solution_code": "def get_status():\n    return {\"status\": \"ok\", \"version\": \"1.0\"}\n\nprint(get_status())",
        "explanation": "Modern Python web frameworks automatically serialize dictionaries into JSON responses.",
        "metadata": {"concept": "json_response_handler", "skill": "api_design", "why_this_exercise_exists": "Replaces filler with JSON route handler"}
    },
    "27.2_q16": {
        "id": "27.2_q16",
        "type": "multiple_choice",
        "concept": "http_post_vs_get",
        "skill": "http_methods",
        "difficulty": "medium",
        "prerequisites": ["27.2_q15"],
        "prompt": "When creating a new resource in a RESTful API, which HTTP method should the route use?",
        "options": [
            "POST",
            "GET",
            "DELETE",
            "HEAD"
        ],
        "correct_answer": "POST",
        "explanation": "REST architecture reserves `GET` for idempotent data reads and `POST` for submitting entity payloads to create new resources.",
        "metadata": {"concept": "rest_http_verbs", "skill": "http_methods", "why_this_exercise_exists": "Replaces filler with REST HTTP verbs"}
    },
    "27.2_q18": {
        "id": "27.2_q18",
        "type": "code_prediction",
        "concept": "http_status_codes",
        "skill": "status_codes",
        "difficulty": "medium",
        "prerequisites": ["27.2_q17"],
        "prompt": "What HTTP status code represents successful resource creation?",
        "options": [
            "201 Created",
            "200 OK",
            "204 No Content",
            "404 Not Found"
        ],
        "correct_answer": "201 Created",
        "explanation": "`201 Created` indicates that the request succeeded and led to the creation of a new resource on the server.",
        "metadata": {"concept": "http_201_created", "skill": "status_codes", "why_this_exercise_exists": "Replaces filler with HTTP status codes"}
    },

    # 32.1 Array and String Concepts
    "32.1_q13": {
        "id": "32.1_q13",
        "type": "code_prediction",
        "concept": "array_indexing_time_complexity",
        "skill": "complexity",
        "difficulty": "easy",
        "prerequisites": ["32.1_q12"],
        "prompt": "What is the time complexity of accessing an element in a Python list by index (e.g. `arr[i]`)?",
        "options": [
            "O(1) constant time",
            "O(n) linear time",
            "O(log n) logarithmic time",
            "O(n^2) quadratic time"
        ],
        "correct_answer": "O(1) constant time",
        "explanation": "Python lists are contiguous arrays of memory pointers. Finding an element by index requires simple address arithmetic (`base_address + index * pointer_size`), executing in O(1) constant time.",
        "metadata": {"concept": "constant_time_indexing", "skill": "complexity", "why_this_exercise_exists": "Replaces filler with O(1) array access complexity"}
    },
    "32.1_q14": {
        "id": "32.1_q14",
        "type": "code_prediction",
        "concept": "string_join_efficiency",
        "skill": "performance",
        "difficulty": "medium",
        "prerequisites": ["32.1_q13"],
        "prompt": "Why is `''.join(char_list)` vastly faster than repeated string concatenation `s += c` in a loop?",
        "options": [
            "''.join() pre-calculates the exact total buffer size and allocates memory once in O(n) time, whereas s += c reallocates new strings repeatedly taking O(n^2) time.",
            "''.join() uses multiple threads.",
            "s += c only works on numbers.",
            "There is no difference."
        ],
        "correct_answer": "''.join() pre-calculates the exact total buffer size and allocates memory once in O(n) time, whereas s += c reallocates new strings repeatedly taking O(n^2) time.",
        "explanation": "Repeatedly concatenating immutable strings causes quadratic O(n^2) copying. `join()` computes the total length once and constructs the result in linear O(n) time.",
        "metadata": {"concept": "string_join_linear_time", "skill": "performance", "why_this_exercise_exists": "Replaces filler with string concatenation complexity"}
    },
    "32.1_q16": {
        "id": "32.1_q16",
        "type": "output_prediction",
        "concept": "array_slice_copy",
        "skill": "memory_model",
        "difficulty": "medium",
        "prerequisites": ["32.1_q15"],
        "prompt": "Does slicing a list `b = a[:]` create a shallow copy or a reference alias?\n\n```python\na = [1, 2, 3]\nb = a[:]\nb.append(4)\nprint(len(a), len(b))\n```",
        "options": [
            "3 4 (b is a new independent list shallow copy)",
            "4 4 (both alias the same list)",
            "3 3",
            "TypeError"
        ],
        "correct_answer": "3 4 (b is a new independent list shallow copy)",
        "explanation": "Slicing `a[:]` creates a new shallow copy of the list. Mutating `b` does not affect `a`.",
        "metadata": {"concept": "shallow_copy_slicing", "skill": "memory_model", "why_this_exercise_exists": "Replaces filler with shallow copy mechanics"}
    },
    "32.1_q18": {
        "id": "32.1_q18",
        "type": "write_the_code",
        "concept": "array_two_pointer_partition",
        "skill": "dsa_implementation",
        "difficulty": "hard",
        "prerequisites": ["32.1_q17"],
        "prompt": "Write a snippet using two pointers to reverse the list `nums = [10, 20, 30, 40]` in place.",
        "starter_code": "nums = [10, 20, 30, 40]\n# Reverse in place with two pointers\n",
        "solution_code": "nums = [10, 20, 30, 40]\nl, r = 0, len(nums) - 1\nwhile l < r:\n    nums[l], nums[r] = nums[r], nums[l]\n    l += 1\n    r -= 1\nprint(nums)",
        "explanation": "Swapping opposite elements inward reverses the array in O(n) time and O(1) space.",
        "metadata": {"concept": "in_place_two_pointers", "skill": "dsa", "why_this_exercise_exists": "Replaces filler with two-pointer array reversal"}
    },

    # 33.2 Dictionaries as Hash Maps
    "33.2_q13": {
        "id": "33.2_q13",
        "type": "write_the_code",
        "concept": "frequency_map_counting",
        "skill": "hash_maps",
        "difficulty": "medium",
        "prerequisites": ["33.2_q12"],
        "prompt": "Build a character frequency dictionary `freq` for string `text = 'banana'` using `dict.get(char, 0) + 1`.",
        "starter_code": "text = \"banana\"\nfreq = {}\n# Populate frequency dictionary\n",
        "solution_code": "text = \"banana\"\nfreq = {}\nfor char in text:\n    freq[char] = freq.get(char, 0) + 1\nprint(freq)",
        "explanation": "`freq.get(char, 0)` returns the current count or 0 if missing, enabling frequency counting in O(n) time.",
        "metadata": {"concept": "frequency_counting_dict", "skill": "hash_maps", "why_this_exercise_exists": "Replaces filler with frequency map implementation"}
    },
    "33.2_q14": {
        "id": "33.2_q14",
        "type": "code_prediction",
        "concept": "hash_map_lookup_complexity",
        "skill": "complexity",
        "difficulty": "medium",
        "prerequisites": ["33.2_q13"],
        "prompt": "What is the average time complexity of key lookup `key in dict` in a Python dictionary?",
        "options": [
            "O(1) average time",
            "O(n) linear time",
            "O(log n) logarithmic time",
            "O(n^2) quadratic time"
        ],
        "correct_answer": "O(1) average time",
        "explanation": "Python dictionaries use open-addressing hash tables, achieving O(1) average time complexity for key lookups, insertions, and deletions.",
        "metadata": {"concept": "hash_table_lookup_time", "skill": "complexity", "why_this_exercise_exists": "Replaces filler with O(1) hash map complexity"}
    },
    "33.2_q16": {
        "id": "33.2_q16",
        "type": "code_prediction",
        "concept": "two_sum_hash_map_optimization",
        "skill": "algorithmic_patterns",
        "difficulty": "hard",
        "prerequisites": ["33.2_q15"],
        "prompt": "How does using a hash map optimize the classic Two-Sum problem from O(n^2) brute force to O(n)?",
        "options": [
            "By storing visited numbers in a dictionary, the complement (target - num) can be checked in O(1) time during a single pass.",
            "By sorting the dictionary in O(1) time.",
            "By splitting the array into two halves.",
            "By converting the numbers to binary."
        ],
        "correct_answer": "By storing visited numbers in a dictionary, the complement (target - num) can be checked in O(1) time during a single pass.",
        "explanation": "Checking `if (target - num) in seen:` executes in O(1) average time, reducing the pair search from nested O(n^2) loops to a single O(n) linear scan.",
        "metadata": {"concept": "two_sum_hash_optimization", "skill": "algorithms", "why_this_exercise_exists": "Replaces filler with canonical two-sum hash pattern"}
    },
    "33.2_q18": {
        "id": "33.2_q18",
        "type": "write_the_code",
        "concept": "grouping_by_key_dict",
        "skill": "data_aggregation",
        "difficulty": "hard",
        "prerequisites": ["33.2_q17"],
        "prompt": "Group words `words = ['apple', 'bat', 'ant', 'ball']` by their first letter into a dictionary `groups` using `dict.setdefault(letter, []).append(word)`.",
        "starter_code": "words = [\"apple\", \"bat\", \"ant\", \"ball\"]\ngroups = {}\n# Group words by first letter\n",
        "solution_code": "words = [\"apple\", \"bat\", \"ant\", \"ball\"]\ngroups = {}\nfor w in words:\n    groups.setdefault(w[0], []).append(w)\nprint(groups)",
        "explanation": "`setdefault(key, [])` initializes the list if the key is new and appends the word, creating `{'a': ['apple', 'ant'], 'b': ['bat', 'ball']}`.",
        "metadata": {"concept": "setdefault_grouping", "skill": "data_aggregation", "why_this_exercise_exists": "Replaces filler with hash map grouping"}
    },

    # 39.3 Breadth-First Search (BFS)
    "39.3_q13": {
        "id": "39.3_q13",
        "type": "code_prediction",
        "concept": "bfs_queue_data_structure",
        "skill": "data_structures",
        "difficulty": "medium",
        "prerequisites": ["39.3_q12"],
        "prompt": "Why should BFS use `collections.deque` instead of a standard Python `list` for its queue?",
        "options": [
            "deque.popleft() is O(1) constant time, whereas list.pop(0) is O(n) linear time because it shifts all remaining elements in memory.",
            "deque sorts vertices automatically.",
            "Python lists cannot store graph nodes.",
            "deque uses recursive memory."
        ],
        "correct_answer": "deque.popleft() is O(1) constant time, whereas list.pop(0) is O(n) linear time because it shifts all remaining elements in memory.",
        "explanation": "Popping from the left of a standard list takes O(n) time, degrading BFS to O(V^2). A doubly linked `deque` performs `popleft()` in O(1) time.",
        "metadata": {"concept": "deque_popleft_efficiency", "skill": "data_structures", "why_this_exercise_exists": "Replaces filler with BFS deque performance"}
    },
    "39.3_q14": {
        "id": "39.3_q14",
        "type": "error_diagnosis",
        "concept": "bfs_visited_set_necessity",
        "skill": "graph_algorithms",
        "difficulty": "medium",
        "prerequisites": ["39.3_q13"],
        "prompt": "What happens if a BFS traversal on a graph with cycles omits the `visited` set?",
        "options": [
            "It enters an infinite loop, cycling between connected nodes forever.",
            "It crashes with IndexError.",
            "It converts to DFS automatically.",
            "It drops all directed edges."
        ],
        "correct_answer": "It enters an infinite loop, cycling between connected nodes forever.",
        "explanation": "Without tracking visited nodes, BFS will re-add previously processed neighbors to the queue repeatedly in cyclic graphs, causing an infinite loop or memory exhaustion.",
        "metadata": {"concept": "visited_set_cycle_prevention", "skill": "graph_algorithms", "why_this_exercise_exists": "Replaces filler with cycle prevention in BFS"}
    },
    "39.3_q16": {
        "id": "39.3_q16",
        "type": "write_the_code",
        "concept": "bfs_traversal_implementation",
        "skill": "graph_traversal",
        "difficulty": "hard",
        "prerequisites": ["39.3_q15"],
        "prompt": "Implement a basic BFS traversal `bfs(graph, start)` using `collections.deque` and a `visited` set that returns the list of visited nodes in visitation order.",
        "starter_code": "from collections import deque\n\ndef bfs(graph, start):\n    # Return list of visited nodes\n    pass",
        "solution_code": "from collections import deque\n\ndef bfs(graph, start):\n    visited = set([start])\n    queue = deque([start])\n    order = []\n    while queue:\n        node = queue.popleft()\n        order.append(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n    return order\n\ng = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}\nprint(bfs(g, 'A'))",
        "explanation": "BFS initializes with the start node, visits level-by-level using a FIFO queue, and guards against cycles with `visited` set.",
        "metadata": {"concept": "bfs_queue_traversal", "skill": "graph_traversal", "why_this_exercise_exists": "Replaces filler with full BFS implementation"}
    },
    "39.3_q18": {
        "id": "39.3_q18",
        "type": "multiple_choice",
        "concept": "bfs_shortest_path_property",
        "skill": "algorithm_properties",
        "difficulty": "medium",
        "prerequisites": ["39.3_q17"],
        "prompt": "Why is BFS guaranteed to find the shortest path in an UNWEIGHTED graph?",
        "options": [
            "BFS explores nodes in order of their distance (edge count) from the start node, ensuring the first time a target is reached, it is via the fewest possible edges.",
            "BFS evaluates edge weights greedily.",
            "BFS backtracks using a stack.",
            "BFS sorts the adjacency list."
        ],
        "correct_answer": "BFS explores nodes in order of their distance (edge count) from the start node, ensuring the first time a target is reached, it is via the fewest possible edges.",
        "explanation": "Because BFS processes nodes layer by layer (distance 1, then distance 2, etc.), the first time the destination node is discovered is guaranteed to be the minimum edge distance.",
        "metadata": {"concept": "bfs_shortest_path_guarantee", "skill": "algorithm_properties", "why_this_exercise_exists": "Replaces filler with shortest path property"}
    }
}
