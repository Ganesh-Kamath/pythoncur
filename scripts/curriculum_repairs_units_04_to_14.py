"""
CODOLINGO EXACT REPAIRS: UNITS 04 - 14
Defines pedagogically rigorous, validated replacements for:
- Unit 4 (4.1 input, 4.2 numeric input)
- Unit 5 (5.1 if statement, 5.2 else statement, 5.4 nested, 5.6 interactive calculator)
- Unit 6 (6.2 while loops, 6.7 nested loops)
- Unit 7 (7.9 string formatter project)
- Unit 11 (11.3 params/args, 11.4 return values, 11.5 multi-params/returns)
- Unit 12 (12.1 syntax vs runtime, 12.2 tracebacks, 12.3 built-in exceptions, 12.5 debugging)
- Unit 13 (13.1 reading text files, 13.4 writing files)
- Unit 14 (14.1 csv, 14.5 generating json, 14.6 cli expense tracker)
"""

REPLACEMENTS_UNITS_04_TO_14 = {
    # ==========================================
    # UNIT 4: USER INPUT AND OUTPUT
    # ==========================================
    # 4.1 The input() Function
    "4.1_q2": {
        "id": "4.1_q2",
        "type": "output_prediction",
        "concept": "the_input_function_basics",
        "skill": "mental_model",
        "difficulty": "easy",
        "prerequisites": ["4.1_q1"],
        "prompt": "Consider the following code:\n\n```python\nage = input(\"Enter your age: \")\n# User types: 25\nprint(type(age))\n```\n\nWhat is printed to the console?",
        "options": [
            "<class 'str'>",
            "<class 'int'>",
            "<class 'float'>",
            "TypeError"
        ],
        "correct_answer": "<class 'str'>",
        "explanation": "In Python, the `input()` function ALWAYS returns user entry as a string (`str`), even if the user types digits. To treat the input as a number, it must be explicitly converted using `int()` or `float()`.",
        "metadata": {
            "concept": "input_return_type",
            "skill": "type_awareness",
            "learning_objective": "Understand that input() always produces a string",
            "common_misconception": "Believing numeric keyboard input automatically becomes an int",
            "why_this_exercise_exists": "Prevents catastrophic type errors when performing arithmetic on raw input"
        }
    },
    "4.1_q4": {
        "id": "4.1_q4",
        "type": "code_prediction",
        "concept": "the_input_function_basics",
        "skill": "input_handling",
        "difficulty": "easy",
        "prerequisites": ["4.1_q3"],
        "prompt": "Consider this code where the user enters their name with extra spaces around it:\n\n```python\nraw_name = \"  Aria  \"\ncleaned_name = raw_name.strip()\nprint(f\"Welcome, [{cleaned_name}]!\")\n```\n\nWhat is the exact output?",
        "options": [
            "Welcome, [Aria]!",
            "Welcome, [  Aria  ]!",
            "Welcome, [Aria ]!",
            "SyntaxError"
        ],
        "correct_answer": "Welcome, [Aria]!",
        "explanation": "User input frequently contains accidental leading or trailing whitespace. Calling `.strip()` returns a new string with surrounding whitespace removed, which is crucial for clean data processing.",
        "metadata": {
            "concept": "input_whitespace_cleaning",
            "skill": "data_sanitization",
            "learning_objective": "Sanitize user string input using strip()",
            "common_misconception": "Assuming input() automatically trims surrounding spaces",
            "why_this_exercise_exists": "Teaches fundamental input hygiene before storing or checking user strings"
        }
    },
    "4.1_q5": {
        "id": "4.1_q5",
        "type": "fix_the_code",
        "concept": "the_input_function_basics",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["4.1_q4"],
        "prompt": "The following program intends to greet the user with punctuation, but currently prints `Hello  Ganesh !` with awkward double spaces. Fix the concatenation or string formatting so it cleanly outputs `Hello Ganesh!` without extra spaces.\n\n```python\nname = \"Ganesh\"\n# Fix this line:\ngreeting = \"Hello \" + \" \" + name + \" !\"\nprint(greeting)\n```",
        "starter_code": "name = \"Ganesh\"\ngreeting = \"Hello \" + \" \" + name + \" !\"\nprint(greeting)",
        "solution_code": "name = \"Ganesh\"\ngreeting = f\"Hello {name}!\"\nprint(greeting)",
        "explanation": "Using f-strings (`f\"Hello {name}!\"`) avoids fragile plus-operator concatenation and allows precise control over spacing and punctuation around injected variables.",
        "metadata": {
            "concept": "string_formatting_for_prompts",
            "skill": "string_construction",
            "learning_objective": "Construct clean greetings from user variables without spacing bugs",
            "common_misconception": "Relying on manual plus concatenation leading to awkward spacing",
            "why_this_exercise_exists": "Ensures polished CLI user interfaces"
        }
    },
    "4.1_q6": {
        "id": "4.1_q6",
        "type": "output_prediction",
        "concept": "the_input_function_basics",
        "skill": "tracing",
        "difficulty": "medium",
        "prerequisites": ["4.1_q5"],
        "prompt": "What does the following snippet output when the user provides `\"Dev\"` for first name and `\"Roy\"` for last name?\n\n```python\nfirst = \"Dev\"\nlast = \"Roy\"\nfull_greeting = f\"User: {last.upper()}, {first.capitalize()}\"\nprint(full_greeting)\n```",
        "options": [
            "User: ROY, Dev",
            "User: Roy, Dev",
            "User: ROY, DEV",
            "User: Dev, Roy"
        ],
        "correct_answer": "User: ROY, Dev",
        "explanation": "`last.upper()` transforms `'Roy'` to `'ROY'`, while `first.capitalize()` ensures `'Dev'` starts with an uppercase letter and the rest lowercase. The f-string formats them as `'User: ROY, Dev'`.",
        "metadata": {
            "concept": "input_formatting_pipeline",
            "skill": "string_transformation",
            "learning_objective": "Combine input variables with case normalization methods",
            "common_misconception": "Confusing upper() and capitalize()",
            "why_this_exercise_exists": "Shows how raw input strings are normalized for display or indexing"
        }
    },
    "4.1_q10": {
        "id": "4.1_q10",
        "type": "write_the_code",
        "concept": "the_input_function_basics",
        "skill": "construction",
        "difficulty": "medium",
        "prerequisites": ["4.1_q9"],
        "prompt": "Write a complete program snippet that stores a first name `'Maya'` and a last name `'Lin'`, strips any whitespace, and constructs a clean greeting string `'Greetings, Maya Lin!'` stored in a variable called `greeting`.",
        "starter_code": "first = \"  Maya \"\nlast = \" Lin  \"\n# Strip whitespace and build greeting\n",
        "solution_code": "first = \"  Maya \"\nlast = \" Lin  \"\ngreeting = f\"Greetings, {first.strip()} {last.strip()}!\"\nprint(greeting)",
        "explanation": "Calling `.strip()` on both `first` and `last` removes unintentional leading/trailing whitespace before interpolating them into the formatted greeting.",
        "metadata": {
            "concept": "input_sanitization_and_assembly",
            "skill": "implementation",
            "learning_objective": "Implement an end-to-end user input normalization routine",
            "common_misconception": "Overlooking whitespace inside user inputs",
            "why_this_exercise_exists": "Builds authentic CLI data collection skills"
        }
    },

    # 4.2 Processing Numeric Input
    "4.2_q2": {
        "id": "4.2_q2",
        "type": "error_diagnosis",
        "concept": "processing_numeric_input_basics",
        "skill": "debugging",
        "difficulty": "easy",
        "prerequisites": ["4.2_q1"],
        "prompt": "A developer writes the following code to compute next year's age:\n\n```python\nage = \"19\"  # Simulating raw return from input()\nnext_age = age + 1\nprint(next_age)\n```\n\nWhat error occurs when this code executes and why?",
        "options": [
            "TypeError: can only concatenate str (not \"int\") to str",
            "ValueError: invalid literal for int() with base 10",
            "SyntaxError: cannot add number to variable",
            "ZeroDivisionError: division by zero"
        ],
        "correct_answer": "TypeError: can only concatenate str (not \"int\") to str",
        "explanation": "Because `age` is a string (`\"19\"`), Python refuses to add an integer (`1`) using the `+` operator. Python does not automatically coerce strings to numbers in addition; you must explicitly cast with `int(age)`.",
        "metadata": {
            "concept": "string_numeric_type_mismatch",
            "skill": "error_recognition",
            "learning_objective": "Recognize why raw input cannot participate in arithmetic",
            "common_misconception": "Assuming Python automatically casts numeric strings to numbers during addition",
            "why_this_exercise_exists": "The #1 beginner bug when handling user input in Python"
        }
    },
    "4.2_q4": {
        "id": "4.2_q4",
        "type": "fix_the_code",
        "concept": "processing_numeric_input_basics",
        "skill": "repair",
        "difficulty": "easy",
        "prerequisites": ["4.2_q3"],
        "prompt": "Fix the following code so that it correctly converts the input string `items_str` into an integer and calculates `total_items` by adding 5.\n\n```python\nitems_str = \"12\"\n# Fix this calculation:\ntotal_items = items_str + 5\nprint(total_items)\n```",
        "starter_code": "items_str = \"12\"\ntotal_items = items_str + 5\nprint(total_items)",
        "solution_code": "items_str = \"12\"\ntotal_items = int(items_str) + 5\nprint(total_items)",
        "explanation": "Wrapping `items_str` with `int(items_str)` converts the string `'12'` to the integer `12`. Now `12 + 5` evaluates to `17` without a TypeError.",
        "metadata": {
            "concept": "int_conversion",
            "skill": "type_casting",
            "learning_objective": "Convert numeric strings to integers using int()",
            "common_misconception": "Trying to cast the entire expression instead of the input string",
            "why_this_exercise_exists": "Instills proper type conversion habits"
        }
    },
    "4.2_q5": {
        "id": "4.2_q5",
        "type": "output_prediction",
        "concept": "processing_numeric_input_basics",
        "skill": "tracing",
        "difficulty": "medium",
        "prerequisites": ["4.2_q4"],
        "prompt": "Consider processing a floating point price input:\n\n```python\nprice_input = \"19.95\"\nquantity = 2\ntotal = float(price_input) * quantity\nprint(f\"Total: ${total:.2f}\")\n```\n\nWhat is the exact output printed?",
        "options": [
            "Total: $39.90",
            "Total: $39.9",
            "Total: $19.9519.95",
            "TypeError: cannot multiply float by int"
        ],
        "correct_answer": "Total: $39.90",
        "explanation": "`float(\"19.95\")` converts the string to `19.95`. Multiplying by `2` yields `39.9`. The format specifier `:.2f` rounds/formats the floating point number to exactly two decimal places (`$39.90`).",
        "metadata": {
            "concept": "float_conversion_and_formatting",
            "skill": "float_arithmetic",
            "learning_objective": "Parse decimal string input with float() and format currency output",
            "common_misconception": "Using int() on decimal strings which raises ValueError",
            "why_this_exercise_exists": "Crucial for handling monetary and fractional input in CLI apps"
        }
    },
    "4.2_q6": {
        "id": "4.2_q6",
        "type": "error_diagnosis",
        "concept": "processing_numeric_input_basics",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["4.2_q5"],
        "prompt": "What happens if a user types `\"25.5\"` and your code executes `int(user_text)` directly?\n\n```python\nuser_text = \"25.5\"\nval = int(user_text)\n```",
        "options": [
            "Raises ValueError: invalid literal for int() with base 10: '25.5'",
            "Truncates to integer 25 automatically",
            "Rounds up to 26",
            "Converts to float 25.5 silently"
        ],
        "correct_answer": "Raises ValueError: invalid literal for int() with base 10: '25.5'",
        "explanation": "`int()` only parses strings that contain integer digits (and an optional +/- sign). A decimal point `.` is not a valid base-10 integer character, causing Python to raise a `ValueError`. To parse decimals, use `float(user_text)`.",
        "metadata": {
            "concept": "int_float_parsing_boundary",
            "skill": "exception_understanding",
            "learning_objective": "Understand when int() fails on decimal strings",
            "common_misconception": "Assuming int('25.5') will truncate to 25 like int(25.5) does",
            "why_this_exercise_exists": "Disabuses the learner of the subtle difference between int(float_val) and int(str_val)"
        }
    },
    "4.2_q10": {
        "id": "4.2_q10",
        "type": "write_the_code",
        "concept": "processing_numeric_input_basics",
        "skill": "construction",
        "difficulty": "medium",
        "prerequisites": ["4.2_q9"],
        "prompt": "Write a snippet that takes a string `bill_str = \"45.50\"` and `tip_percent = 20`, converts `bill_str` to float, calculates the tip amount (`bill * tip_percent / 100`), and stores the rounded total (`bill + tip`) in a variable `final_bill` formatted to 2 decimals.",
        "starter_code": "bill_str = \"45.50\"\ntip_percent = 20\n# Convert, calculate tip and final_bill\n",
        "solution_code": "bill_str = \"45.50\"\ntip_percent = 20\nbill = float(bill_str)\ntip = bill * (tip_percent / 100)\nfinal_bill = round(bill + tip, 2)\nprint(f\"${final_bill:.2f}\")",
        "explanation": "`float(bill_str)` yields `45.5`. Tip is `45.5 * 0.20 = 9.1`. Adding them gives `54.6`, which rounded to 2 decimal places produces `54.60`.",
        "metadata": {
            "concept": "numeric_input_pipeline",
            "skill": "application",
            "learning_objective": "Construct an end-to-end numerical calculation from string inputs",
            "common_misconception": "Forgetting to convert string before arithmetic",
            "why_this_exercise_exists": "Provides genuine practical application for user input calculations"
        }
    },

    # ==========================================
    # UNIT 5: CONDITIONAL LOGIC
    # ==========================================
    # 5.1 The if Statement
    "5.1_q2": {
        "id": "5.1_q2",
        "type": "output_prediction",
        "concept": "the_if_statement_basics",
        "skill": "mental_model",
        "difficulty": "easy",
        "prerequisites": ["5.1_q1"],
        "prompt": "Predict the output of the following conditional block:\n\n```python\ntemperature = 22\nif temperature > 20:\n    print(\"Pleasant weather\")\nprint(\"Done\")\n```",
        "options": [
            "Pleasant weather\nDone",
            "Pleasant weather",
            "Done",
            "No output is printed"
        ],
        "correct_answer": "Pleasant weather\nDone",
        "explanation": "Since `22 > 20` evaluates to `True`, the indented body under `if` executes, printing `'Pleasant weather'`. Then execution continues sequentially outside the `if` block, printing `'Done'`.",
        "metadata": {
            "concept": "if_execution_flow",
            "skill": "control_flow",
            "learning_objective": "Trace execution through an if block and subsequent statements",
            "common_misconception": "Thinking code after an if block only runs when the condition is False",
            "why_this_exercise_exists": "Reinforces python block structure and sequential execution"
        }
    },
    "5.1_q4": {
        "id": "5.1_q4",
        "type": "error_diagnosis",
        "concept": "the_if_statement_basics",
        "skill": "debugging",
        "difficulty": "easy",
        "prerequisites": ["5.1_q3"],
        "prompt": "Examine this Python snippet:\n\n```python\nage = 18\nif age >= 18:\nprint(\"Adult\")\n```\n\nWhy will Python fail to execute this code?",
        "options": [
            "IndentationError: expected an indented block after 'if' statement",
            "SyntaxError: invalid comparison operator",
            "TypeError: 'age' is not defined",
            "ValueError: condition cannot evaluate equality"
        ],
        "correct_answer": "IndentationError: expected an indented block after 'if' statement",
        "explanation": "Python uses indentation (standard 4 spaces) rather than curly braces `{}` to determine which statements belong inside an `if` block. An unindented statement immediately following an `if` header triggers an `IndentationError`.",
        "metadata": {
            "concept": "if_block_indentation",
            "skill": "syntax_debugging",
            "learning_objective": "Identify and diagnose IndentationError in conditional statements",
            "common_misconception": "Assuming whitespace is purely aesthetic in Python",
            "why_this_exercise_exists": "Core Python structural rule that every programmer must master"
        }
    },
    "5.1_q5": {
        "id": "5.1_q5",
        "type": "code_prediction",
        "concept": "the_if_statement_basics",
        "skill": "boundary_analysis",
        "difficulty": "medium",
        "prerequisites": ["5.1_q4"],
        "prompt": "A grading script checks student scores:\n\n```python\nscore = 90\nif score > 90:\n    print(\"Honor Roll\")\nprint(\"Processed\")\n```\n\nWhat is printed to the console when `score` is exactly 90?",
        "options": [
            "Processed",
            "Honor Roll\nProcessed",
            "Honor Roll",
            "Nothing"
        ],
        "correct_answer": "Processed",
        "explanation": "The strict greater-than operator `>` checks if `90 > 90`, which is `False`! Therefore, the indented block is skipped entirely, and only `'Processed'` is printed. If 90 was meant to qualify, the condition should use `>=`.",
        "metadata": {
            "concept": "strict_vs_inclusive_inequality",
            "skill": "boundary_testing",
            "learning_objective": "Discriminate between strict (>) and inclusive (>=) comparison boundaries",
            "common_misconception": "Treating > as including the boundary value",
            "why_this_exercise_exists": "Boundary/off-by-one errors in conditionals are a primary source of business logic bugs"
        }
    },
    "5.1_q6": {
        "id": "5.1_q6",
        "type": "fix_the_code",
        "concept": "the_if_statement_basics",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["5.1_q5"],
        "prompt": "Fix the indentation in the code below so that the discount message only prints when `cart_total` exceeds 100, but the checkout message always prints.\n\n```python\ncart_total = 75\nif cart_total > 100:\nprint(\"Free shipping applied!\")\nprint(\"Ready for checkout\")\n```",
        "starter_code": "cart_total = 75\nif cart_total > 100:\nprint(\"Free shipping applied!\")\nprint(\"Ready for checkout\")",
        "solution_code": "cart_total = 75\nif cart_total > 100:\n    print(\"Free shipping applied!\")\nprint(\"Ready for checkout\")",
        "explanation": "Indenting `print(\"Free shipping applied!\")` by 4 spaces places it inside the `if` body, so it only executes when `cart_total > 100`. Leaving `print(\"Ready for checkout\")` unindented ensures it executes regardless of the cart total.",
        "metadata": {
            "concept": "conditional_scoping",
            "skill": "indentation_control",
            "learning_objective": "Scope statements correctly inside and outside an if statement",
            "common_misconception": "Indenting all subsequent lines or indenting none",
            "why_this_exercise_exists": "Directly trains visual and cognitive reasoning about Python blocks"
        }
    },
    "5.1_q10": {
        "id": "5.1_q10",
        "type": "write_the_code",
        "concept": "the_if_statement_basics",
        "skill": "construction",
        "difficulty": "medium",
        "prerequisites": ["5.1_q9"],
        "prompt": "Write an `if` statement that checks if `temperature` is greater than 30. If true, set `alert` to `'Heat advisory'` and print `'Drink water'`. If `temperature` is 32, execute the check.",
        "starter_code": "temperature = 32\nalert = \"Normal\"\n# Write the if statement here\n",
        "solution_code": "temperature = 32\nalert = \"Normal\"\nif temperature > 30:\n    alert = \"Heat advisory\"\n    print(\"Drink water\")",
        "explanation": "`temperature > 30` evaluates to `True` for 32. Inside the indented block, `alert` is updated to `'Heat advisory'` and `'Drink water'` is printed.",
        "metadata": {
            "concept": "state_mutation_in_if",
            "skill": "implementation",
            "learning_objective": "Mutate program state conditionally inside an if block",
            "common_misconception": "Forgetting the colon at the end of the if header",
            "why_this_exercise_exists": "Teaches fundamental decision-making and state tracking"
        }
    },
    "5.1_q13": {
        "id": "5.1_q13",
        "type": "output_prediction",
        "concept": "the_if_statement_basics",
        "skill": "mental_model",
        "difficulty": "medium",
        "prerequisites": ["5.1_q12"],
        "prompt": "What does this code output when `battery_level` is 15?\n\n```python\nbattery_level = 15\nif battery_level <= 20:\n    print(\"Low Battery\")\nif battery_level <= 10:\n    print(\"Critical Battery\")\n```",
        "options": [
            "Low Battery",
            "Low Battery\nCritical Battery",
            "Critical Battery",
            "No output"
        ],
        "correct_answer": "Low Battery",
        "explanation": "The first condition `15 <= 20` is `True`, so `'Low Battery'` prints. The second condition `15 <= 10` is `False`, so the second block is skipped.",
        "metadata": {
            "concept": "independent_if_evaluation",
            "skill": "branching_logic",
            "learning_objective": "Understand that sequential if statements evaluate independently",
            "common_misconception": "Confusing sequential if statements with mutually exclusive if-elif chains",
            "why_this_exercise_exists": "Prevents logic bugs where multiple if statements accidentally trigger"
        }
    },
    "5.1_q14": {
        "id": "5.1_q14",
        "type": "fix_the_code",
        "concept": "the_if_statement_basics",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["5.1_q13"],
        "prompt": "The code below attempts to check if a username has at least 3 characters, but uses an assignment `=` instead of an equality comparison `==`. Fix the code.\n\n```python\nusername = \"sam\"\n# Fix the condition to check if username is \"admin\"\nis_admin = False\nif username = \"admin\":\n    is_admin = True\n```",
        "starter_code": "username = \"sam\"\nis_admin = False\nif username = \"admin\":\n    is_admin = True",
        "solution_code": "username = \"sam\"\nis_admin = False\nif username == \"admin\":\n    is_admin = True",
        "explanation": "In Python, a single `=` is the assignment operator, which is illegal syntax in an `if` expression. The equality operator `==` compares whether `username` equals `'admin'`.",
        "metadata": {
            "concept": "assignment_vs_equality",
            "skill": "syntax_repair",
            "learning_objective": "Distinguish assignment (=) from equality comparison (==) in conditions",
            "common_misconception": "Using single = inside an if statement",
            "why_this_exercise_exists": "Eliminates one of the most common syntax errors across all programming languages"
        }
    },

    # 5.2 The else Statement
    "5.2_q2": {
        "id": "5.2_q2",
        "type": "output_prediction",
        "concept": "the_else_statement_basics",
        "skill": "mental_model",
        "difficulty": "easy",
        "prerequisites": ["5.2_q1"],
        "prompt": "Trace the execution of this `if-else` structure:\n\n```python\naccount_balance = 45\nitem_cost = 50\n\nif account_balance >= item_cost:\n    print(\"Purchase approved\")\nelse:\n    print(\"Insufficient funds\")\n```\n\nWhat is output to the terminal?",
        "options": [
            "Insufficient funds",
            "Purchase approved",
            "Purchase approved\nInsufficient funds",
            "SyntaxError"
        ],
        "correct_answer": "Insufficient funds",
        "explanation": "Because `45 >= 50` evaluates to `False`, Python completely skips the `if` body and executes the `else` branch, printing `'Insufficient funds'`.",
        "metadata": {
            "concept": "if_else_mutual_exclusion",
            "skill": "branch_prediction",
            "learning_objective": "Recognize that exactly one branch executes in an if-else structure",
            "common_misconception": "Thinking both branches can execute or both can be skipped",
            "why_this_exercise_exists": "Foundation of two-way conditional branching"
        }
    },
    "5.2_q4": {
        "id": "5.2_q4",
        "type": "error_diagnosis",
        "concept": "the_else_statement_basics",
        "skill": "debugging",
        "difficulty": "easy",
        "prerequisites": ["5.2_q3"],
        "prompt": "Identify the syntax error in this code snippet:\n\n```python\nage = 16\nif age >= 18:\n    print(\"Adult\")\nelse age < 18:\n    print(\"Minor\")\n```",
        "options": [
            "SyntaxError: 'else' cannot take a condition",
            "TypeError: comparison operator invalid",
            "IndentationError: unexpected indent",
            "NameError: 'Minor' is not defined"
        ],
        "correct_answer": "SyntaxError: 'else' cannot take a condition",
        "explanation": "In Python, an `else` statement acts as a catch-all for when the `if` condition is `False`. It cannot have an expression or condition following it. If you need a condition, use `elif age < 18:`.",
        "metadata": {
            "concept": "else_syntax_rules",
            "skill": "syntax_debugging",
            "learning_objective": "Recognize that else is unconditional; elif is required for additional conditions",
            "common_misconception": "Attempting to supply a condition directly to an else clause",
            "why_this_exercise_exists": "Prevents pervasive syntax errors among beginner programmers"
        }
    },
    "5.2_q5": {
        "id": "5.2_q5",
        "type": "code_prediction",
        "concept": "the_else_statement_basics",
        "skill": "edge_case_reasoning",
        "difficulty": "medium",
        "prerequisites": ["5.2_q4"],
        "prompt": "What does this snippet print when `items` is an empty list `[]`?\n\n```python\nitems = []\nif items:\n    print(f\"Cart has {len(items)} items\")\nelse:\n    print(\"Cart is empty\")\n```",
        "options": [
            "Cart is empty",
            "Cart has 0 items",
            "IndexError",
            "None"
        ],
        "correct_answer": "Cart is empty",
        "explanation": "In Python, empty collections (such as empty lists `[]`, strings `\"\"`, or dicts `{}`) evaluate to `False` in a boolean context (truthiness). Thus, the `if` condition fails and the `else` branch executes.",
        "metadata": {
            "concept": "truthiness_in_conditionals",
            "skill": "idiomatic_python",
            "learning_objective": "Leverage collection truthiness in if-else constructs",
            "common_misconception": "Thinking len(items) == 0 must always be written explicitly",
            "why_this_exercise_exists": "Teaches idiomatic Python truthy/falsy evaluation"
        }
    },
    "5.2_q6": {
        "id": "5.2_q6",
        "type": "fix_the_code",
        "concept": "the_else_statement_basics",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["5.2_q5"],
        "prompt": "Fix the indentation so that the `else` clause properly aligns with the `if` statement:\n\n```python\nstatus_code = 404\nif status_code == 200:\n    print(\"Success\")\n    else:\n    print(\"Error occurred\")\n```",
        "starter_code": "status_code = 404\nif status_code == 200:\n    print(\"Success\")\n    else:\n    print(\"Error occurred\")",
        "solution_code": "status_code = 404\nif status_code == 200:\n    print(\"Success\")\nelse:\n    print(\"Error occurred\")",
        "explanation": "The `else:` clause must be aligned at the exact same indentation level as its matching `if:` statement (column 0 in this case). Indenting `else:` causes a SyntaxError.",
        "metadata": {
            "concept": "else_clause_alignment",
            "skill": "block_alignment",
            "learning_objective": "Properly align else with its corresponding if statement",
            "common_misconception": "Indenting else along with the if body statements",
            "why_this_exercise_exists": "Ensures structural cleanliness in multi-branch statements"
        }
    },
    "5.2_q10": {
        "id": "5.2_q10",
        "type": "write_the_code",
        "concept": "the_else_statement_basics",
        "skill": "construction",
        "difficulty": "medium",
        "prerequisites": ["5.2_q9"],
        "prompt": "Write an `if-else` statement that checks if `password_length >= 8`. If `True`, set `result = \"Valid\"`. Otherwise, set `result = \"Too short\"`. Test with `password_length = 6`.",
        "starter_code": "password_length = 6\n# Write if-else below:\n",
        "solution_code": "password_length = 6\nif password_length >= 8:\n    result = \"Valid\"\nelse:\n    result = \"Too short\"\nprint(result)",
        "explanation": "Since `6 >= 8` is `False`, the `else` branch assigns `'Too short'` to `result`.",
        "metadata": {
            "concept": "binary_decision_logic",
            "skill": "implementation",
            "learning_objective": "Implement two-way decision logic using if-else",
            "common_misconception": "Overcomplicating binary logic with redundant checks",
            "why_this_exercise_exists": "Builds confidence constructing valid validation logic"
        }
    },
    "5.2_q13": {
        "id": "5.2_q13",
        "type": "output_prediction",
        "concept": "the_else_statement_basics",
        "skill": "logic_tracing",
        "difficulty": "medium",
        "prerequisites": ["5.2_q12"],
        "prompt": "What is printed by this ternary (conditional expression) statement?\n\n```python\nscore = 55\nstatus = \"Pass\" if score >= 60 else \"Retake\"\nprint(status)\n```",
        "options": [
            "Retake",
            "Pass",
            "Pass Retake",
            "SyntaxError"
        ],
        "correct_answer": "Retake",
        "explanation": "Python's conditional expression evaluates `X if CONDITION else Y`. Because `55 >= 60` is `False`, it returns `'Retake'`.",
        "metadata": {
            "concept": "ternary_conditional_expression",
            "skill": "idiomatic_branching",
            "learning_objective": "Read and trace single-line if-else expressions",
            "common_misconception": "Thinking the condition is evaluated after the else value",
            "why_this_exercise_exists": "Prepares learners to read real-world concise Python code"
        }
    },
    "5.2_q14": {
        "id": "5.2_q14",
        "type": "fix_the_code",
        "concept": "the_else_statement_basics",
        "skill": "refactoring",
        "difficulty": "medium",
        "prerequisites": ["5.2_q13"],
        "prompt": "Refactor the redundant `if-else` code below to directly return the boolean comparison instead of branching unnecessarily:\n\n```python\ndef is_even(num):\n    if num % 2 == 0:\n        return True\n    else:\n        return False\n```",
        "starter_code": "def is_even(num):\n    if num % 2 == 0:\n        return True\n    else:\n        return False",
        "solution_code": "def is_even(num):\n    return num % 2 == 0",
        "explanation": "`num % 2 == 0` already evaluates to a boolean (`True` or `False`). Writing `if condition: return True else: return False` is an anti-pattern; returning `condition` directly is cleaner, faster, and more pythonic.",
        "metadata": {
            "concept": "boolean_expression_simplification",
            "skill": "clean_code",
            "learning_objective": "Simplify redundant if-else constructs that merely return booleans",
            "common_misconception": "Thinking return statements must always be wrapped in if-else",
            "why_this_exercise_exists": "Transforms beginner syntax into clean, professional code"
        }
    },

    # 5.4 Nested Conditions
    "5.4_q24": {
        "id": "5.4_q24",
        "type": "refactoring_challenge",
        "concept": "nested_conditions_simplification",
        "skill": "refactoring",
        "difficulty": "hard",
        "prerequisites": ["5.4_q23"],
        "prompt": "The following nested conditional code handles venue admission, but is deeply nested and repetitive. Refactor it using clear guard clauses or boolean operators (`and`) to cleanly determine whether entry is allowed, requires ID, or is rejected for age.\n\n```python\nage = 20\nhas_id = False\n\n# Nested version:\nif age >= 18:\n    if has_id:\n        status = \"Allowed\"\n    else:\n        status = \"Requires ID\"\nelse:\n    status = \"Underage\"\nprint(status)\n```",
        "starter_code": "age = 20\nhas_id = False\n# Refactor to clean, readable branching\nif age < 18:\n    status = \"Underage\"\nelif not has_id:\n    status = \"Requires ID\"\nelse:\n    status = \"Allowed\"\nprint(status)",
        "solution_code": "age = 20\nhas_id = False\nif age < 18:\n    status = \"Underage\"\nelif not has_id:\n    status = \"Requires ID\"\nelse:\n    status = \"Allowed\"\nprint(status)",
        "explanation": "Using guard clauses (`age < 18`, then `not has_id`, then fallback to `\"Allowed\"`) flattens the nested indentation pyramid, making conditions easier to read, test, and debug.",
        "metadata": {
            "concept": "guard_clauses_vs_nesting",
            "skill": "architecture",
            "learning_objective": "Flatten deeply nested conditionals using guard clauses and elif",
            "common_misconception": "Assuming nested if blocks are always required for multi-factor decisions",
            "why_this_exercise_exists": "Directly addresses the 'arrow anti-pattern' in nested logic"
        }
    },

    # 5.6 Project: Interactive Calculator
    "5.6_q3": {
        "id": "5.6_q3",
        "type": "code_prediction",
        "concept": "project_interactive_calculator_parsing",
        "skill": "data_validation",
        "difficulty": "medium",
        "prerequisites": ["5.6_q2"],
        "prompt": "In an interactive calculator, a user enters the operator string `\"+\"`. Which conditional structure cleanly identifies the valid operation?\n\n```python\nop = \"+\"\nif op in ('+', '-', '*', '/'):\n    valid = True\nelse:\n    valid = False\nprint(valid)\n```\n\nWhat is output?",
        "options": [
            "True",
            "False",
            "TypeError",
            "None"
        ],
        "correct_answer": "True",
        "explanation": "Checking `op in ('+', '-', '*', '/')` uses the `in` operator to test membership against a collection of valid operators in a single, clear check.",
        "metadata": {
            "concept": "operator_membership_validation",
            "skill": "validation",
            "learning_objective": "Validate user-supplied operators using collection membership",
            "common_misconception": "Writing op == '+' or op == '-' or op == '*' or op == '/'",
            "why_this_exercise_exists": "Replaces synthetic template function with calculator operator validation"
        }
    },
    "5.6_q4": {
        "id": "5.6_q4",
        "type": "error_diagnosis",
        "concept": "project_interactive_calculator_division",
        "skill": "edge_cases",
        "difficulty": "medium",
        "prerequisites": ["5.6_q3"],
        "prompt": "What happens if a calculator performs division without checking the denominator?\n\n```python\nnum1 = 10\nnum2 = 0\nresult = num1 / num2\n```",
        "options": [
            "Raises ZeroDivisionError: division by zero",
            "Returns infinity (float('inf'))",
            "Returns None",
            "Returns 0"
        ],
        "correct_answer": "Raises ZeroDivisionError: division by zero",
        "explanation": "Python does not permit mathematical division by zero. Attempting `num1 / 0` immediately raises `ZeroDivisionError`. Production calculators must guard against this condition prior to division.",
        "metadata": {
            "concept": "zero_division_guard",
            "skill": "defensive_programming",
            "learning_objective": "Anticipate ZeroDivisionError when designing calculator routines",
            "common_misconception": "Believing Python returns inf or None when dividing by zero",
            "why_this_exercise_exists": "Teaches critical defensive validation for arithmetic apps"
        }
    },
    "5.6_q13": {
        "id": "5.6_q13",
        "type": "write_the_code",
        "concept": "project_interactive_calculator_milestone_1",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["5.6_q12"],
        "prompt": "Calculator Milestone 1: Read two numeric inputs from variables `input_a = '15.5'` and `input_b = '4.5'`, convert both to floats, and compute their sum stored in `sum_result`.",
        "starter_code": "input_a = \"15.5\"\ninput_b = \"4.5\"\n# Convert both inputs to floats and store their sum in sum_result\n",
        "solution_code": "input_a = \"15.5\"\ninput_b = \"4.5\"\nnum_a = float(input_a)\nnum_b = float(input_b)\nsum_result = num_a + num_b\nprint(f\"Result: {sum_result}\")",
        "explanation": "Parsing both raw string inputs with `float()` allows accurate floating-point addition yielding `20.0`.",
        "metadata": {
            "concept": "calculator_input_ingestion",
            "skill": "implementation",
            "learning_objective": "Parse operand strings into floats for calculation",
            "common_misconception": "Performing addition before type conversion",
            "why_this_exercise_exists": "First core milestone of the interactive calculator project"
        }
    },
    "5.6_q14": {
        "id": "5.6_q14",
        "type": "write_the_code",
        "concept": "project_interactive_calculator_milestone_2",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["5.6_q13"],
        "prompt": "Calculator Milestone 2: Given `raw_op = '  *  '`, strip any extra whitespace from the operator and verify if it is one of the supported operators `('+', '-', '*', '/')`. Store boolean validity in `is_valid`.",
        "starter_code": "raw_op = \"  *  \"\nsupported = ('+', '-', '*', '/')\n# Clean raw_op and verify validity\n",
        "solution_code": "raw_op = \"  *  \"\nsupported = ('+', '-', '*', '/')\nop = raw_op.strip()\nis_valid = op in supported\nprint(f\"Operator '{op}' valid: {is_valid}\")",
        "explanation": "Stripping whitespace prevents user keystroke errors like `' + '` from failing validity checks against `supported`.",
        "metadata": {
            "concept": "calculator_operator_parsing",
            "skill": "implementation",
            "learning_objective": "Clean and validate user operators against allowed operations",
            "common_misconception": "Testing raw operator without stripping spaces",
            "why_this_exercise_exists": "Second core milestone of the interactive calculator project"
        }
    },
    "5.6_q15": {
        "id": "5.6_q15",
        "type": "write_the_code",
        "concept": "project_interactive_calculator_milestone_3",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["5.6_q14"],
        "prompt": "Calculator Milestone 3: Implement addition and subtraction dispatch. Given `a = 20`, `b = 8`, and `op = '-'`, compute `result` if `op == '+'` or `op == '-'`. Store the answer in `result`.",
        "starter_code": "a = 20\nb = 8\nop = \"-\"\nresult = None\n# Implement addition and subtraction branch\n",
        "solution_code": "a = 20\nb = 8\nop = \"-\"\nresult = None\nif op == \"+\":\n    result = a + b\nelif op == \"-\":\n    result = a - b\nprint(f\"Calculation: {result}\")",
        "explanation": "An `if-elif` chain branches on `op`. For `'-'`, it evaluates `20 - 8 = 12`.",
        "metadata": {
            "concept": "calculator_additive_dispatch",
            "skill": "implementation",
            "learning_objective": "Implement branching for addition and subtraction operations",
            "common_misconception": "Overlapping operators in sequential if statements",
            "why_this_exercise_exists": "Third core milestone of the interactive calculator project"
        }
    },
    "5.6_q16": {
        "id": "5.6_q16",
        "type": "write_the_code",
        "concept": "project_interactive_calculator_milestone_4",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["5.6_q15"],
        "prompt": "Calculator Milestone 4: Add multiplication and division support. Given `a = 24`, `b = 6`, and `op = '/'`, perform the calculation and store in `result`. Handle `op == '*'` as multiplication.",
        "starter_code": "a = 24\nb = 6\nop = \"/\"\nresult = None\n# Add multiplication and division branching\n",
        "solution_code": "a = 24\nb = 6\nop = \"/\"\nresult = None\nif op == \"*\":\n    result = a * b\nelif op == \"/\":\n    result = a / b\nprint(f\"Calculation: {result}\")",
        "explanation": "Evaluating `op == '/'` executes `24 / 6 = 4.0`.",
        "metadata": {
            "concept": "calculator_multiplicative_dispatch",
            "skill": "implementation",
            "learning_objective": "Implement branching for multiplication and division operations",
            "common_misconception": "Using integer division // when standard calculator precision requires float /",
            "why_this_exercise_exists": "Fourth core milestone of the interactive calculator project"
        }
    },
    "5.6_q17": {
        "id": "5.6_q17",
        "type": "fix_the_code",
        "concept": "project_interactive_calculator_milestone_5",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["5.6_q16"],
        "prompt": "Calculator Milestone 5: Safeguard division against zero. Modify the division branch below so that if `b == 0`, it assigns `\"Error: Division by zero\"` to `error_msg` instead of crashing.\n\n```python\na = 10\nb = 0\nop = \"/\"\nif op == \"/\":\n    result = a / b\n```",
        "starter_code": "a = 10\nb = 0\nop = \"/\"\nresult = None\nerror_msg = None\nif op == \"/\":\n    # Guard against b == 0\n    result = a / b",
        "solution_code": "a = 10\nb = 0\nop = \"/\"\nresult = None\nerror_msg = None\nif op == \"/\":\n    if b == 0:\n        error_msg = \"Error: Division by zero\"\n    else:\n        result = a / b\nprint(error_msg if error_msg else result)",
        "explanation": "Checking `if b == 0:` before attempting `a / b` prevents a program crash and provides graceful user-facing error reporting.",
        "metadata": {
            "concept": "zero_division_handling",
            "skill": "error_handling",
            "learning_objective": "Guard against division by zero gracefully in user applications",
            "common_misconception": "Allowing the runtime exception to unceremoniously crash the CLI loop",
            "why_this_exercise_exists": "Fifth core milestone of the interactive calculator project"
        }
    },
    "5.6_q18": {
        "id": "5.6_q18",
        "type": "write_the_code",
        "concept": "project_interactive_calculator_milestone_6",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["5.6_q17"],
        "prompt": "Calculator Milestone 6: Build the consolidated `calculate(a, b, op)` function that brings all 4 operators together, guards against division by zero, and returns `\"Error: Invalid operator\"` for unknown operations.",
        "starter_code": "def calculate(a, b, op):\n    # Return result or descriptive error string\n    pass",
        "solution_code": "def calculate(a, b, op):\n    if op == \"+\":\n        return a + b\n    elif op == \"-\":\n        return a - b\n    elif op == \"*\":\n        return a * b\n    elif op == \"/\":\n        if b == 0:\n            return \"Error: Division by zero\"\n        return a / b\n    else:\n        return \"Error: Invalid operator\"",
        "explanation": "This complete dispatch function cleanly maps inputs to computations while managing invalid operators and division by zero as well-defined return contracts.",
        "metadata": {
            "concept": "calculator_dispatcher_function",
            "skill": "functional_composition",
            "learning_objective": "Consolidate parsing, dispatch, and edge case handling into a single robust function",
            "common_misconception": "Scattering error checks across multiple disconnected blocks",
            "why_this_exercise_exists": "Sixth core milestone completing the core logic of the calculator project"
        }
    },

    # ==========================================
    # UNIT 6: LOOPS
    # ==========================================
    # 6.2 The while Loop
    "6.2_q14": {
        "id": "6.2_q14",
        "type": "multiple_choice",
        "concept": "the_while_loop_execution_contract",
        "skill": "mental_model",
        "difficulty": "medium",
        "prerequisites": ["6.2_q13"],
        "prompt": "Does Python have a native `do-while` loop that guarantees at least one execution of the loop body?",
        "options": [
            "No; Python has no native do-while loop. A standard while loop tests its condition before the first iteration and may execute zero times.",
            "Yes; using the `do while condition:` syntax.",
            "Yes; adding the `always:` keyword guarantees at least one run.",
            "No; while loops always run at least once regardless of condition."
        ],
        "correct_answer": "No; Python has no native do-while loop. A standard while loop tests its condition before the first iteration and may execute zero times.",
        "explanation": "Unlike C, C++, or Java, Python has NO native `do-while` statement. A Python `while condition:` loop evaluates its condition *prior* to executing the loop body. If the condition is initially `False`, the loop body runs zero times. To emulate a do-while loop in Python, developers idiomatically use `while True:` and break at the end based on a condition.",
        "metadata": {
            "concept": "pre_test_loop_evaluation",
            "skill": "conceptual_rigor",
            "learning_objective": "Understand that Python while loops are pre-test and may execute zero times",
            "common_misconception": "Believing Python has a native do-while construct or guarantees one execution",
            "why_this_exercise_exists": "Directly corrects the flawed prior question and teaches how Python actually evaluates loops"
        }
    },
    "6.2_q19": {
        "id": "6.2_q19",
        "type": "fix_the_code",
        "concept": "the_while_loop_infinite_loops",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["6.2_q18"],
        "prompt": "The following while loop is supposed to print numbers 0 through 4, but it causes an infinite loop because the loop counter is never updated! Fix the bug.\n\n```python\ncount = 0\nwhile count < 5:\n    print(count)\n```",
        "starter_code": "count = 0\nwhile count < 5:\n    print(count)",
        "solution_code": "count = 0\nwhile count < 5:\n    print(count)\n    count += 1",
        "explanation": "A while loop continues executing as long as its condition remains `True`. Because `count` was initialized to 0 and never incremented inside the loop body, `count < 5` stayed `True` forever. Adding `count += 1` increments the counter so it reaches 5 and terminates.",
        "metadata": {
            "concept": "infinite_loop_termination",
            "skill": "debugging",
            "learning_objective": "Diagnose and fix infinite loops caused by missing loop variable increments",
            "common_misconception": "Assuming loops automatically increment integer variables like range() does in for loops",
            "why_this_exercise_exists": "Every programmer must master while loop termination guarantees"
        }
    },
    "6.2_q22": {
        "id": "6.2_q22",
        "type": "fix_the_code",
        "concept": "the_while_loop_boundary_conditions",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["6.2_q21"],
        "prompt": "The following code intends to sum the first 5 natural numbers (1 + 2 + 3 + 4 + 5 = 15), but has an off-by-one bug stopping prematurely at 4. Fix the condition.\n\n```python\ntotal = 0\ni = 1\nwhile i < 5:\n    total += i\n    i += 1\nprint(total)\n```",
        "starter_code": "total = 0\ni = 1\nwhile i < 5:\n    total += i\n    i += 1\nprint(total)",
        "solution_code": "total = 0\ni = 1\nwhile i <= 5:\n    total += i\n    i += 1\nprint(total)",
        "explanation": "Using `i < 5` exits the loop when `i` reaches 5, excluding 5 from the sum (yielding 10). Changing the condition to `i <= 5` includes 5 in the accumulation, producing the correct sum `15`.",
        "metadata": {
            "concept": "off_by_one_boundary_condition",
            "skill": "debugging",
            "learning_objective": "Identify and correct off-by-one boundary errors in while loops",
            "common_misconception": "Using strict < when the boundary item should be included",
            "why_this_exercise_exists": "Off-by-one loop errors are ubiquitous in software engineering"
        }
    },
    "6.2_q24": {
        "id": "6.2_q24",
        "type": "refactoring_challenge",
        "concept": "the_while_loop_idiomatic_search",
        "skill": "refactoring",
        "difficulty": "medium",
        "prerequisites": ["6.2_q23"],
        "prompt": "Refactor this manual index-based while loop into an idiomatic `while True` loop that uses `break` when finding the first negative number in `data`:\n\n```python\ndata = [4, 7, -2, 9]\nfound = None\ni = 0\nwhile i < len(data):\n    if data[i] < 0:\n        found = data[i]\n        break\n    i += 1\nprint(found)\n```",
        "starter_code": "data = [4, 7, -2, 9]\nfound = None\n# Refactor using while True and break\nidx = 0\nwhile True:\n    if idx >= len(data):\n        break\n    if data[idx] < 0:\n        found = data[idx]\n        break\n    idx += 1\nprint(found)",
        "solution_code": "data = [4, 7, -2, 9]\nfound = None\nidx = 0\nwhile True:\n    if idx >= len(data):\n        break\n    if data[idx] < 0:\n        found = data[idx]\n        break\n    idx += 1\nprint(found)",
        "explanation": "Emulating a sentinel loop with `while True` and explicit `break` conditions gives complete control over loop exit points for both match and termination conditions.",
        "metadata": {
            "concept": "while_true_break_pattern",
            "skill": "control_flow",
            "learning_objective": "Structure event/search loops using while True and conditional breaks",
            "common_misconception": "Fearing while True because of infinite loop risks",
            "why_this_exercise_exists": "Teaches the standard Python idiom for do-while and event-driven loops"
        }
    },
    "6.2_q30": {
        "id": "6.2_q30",
        "type": "write_the_code",
        "concept": "the_while_loop_pin_retry_system",
        "skill": "system_design",
        "difficulty": "hard",
        "prerequisites": ["6.2_q29"],
        "prompt": "Mastery Challenge: Implement a simulated PIN authentication system using a while loop. The correct PIN is `'4821'`. Given a list of user attempts `attempts = ['0000', '1234', '4821']`, iterate through attempts. If the PIN matches, set `authenticated = True` and exit immediately. Allow at most 3 attempts; if exhausted without success, set `locked_out = True`. Implement this cleanly.",
        "starter_code": "correct_pin = \"4821\"\nattempts = [\"0000\", \"1234\", \"4821\"]\nauthenticated = False\nlocked_out = False\n# Implement PIN verification loop\n",
        "solution_code": "correct_pin = \"4821\"\nattempts = [\"0000\", \"1234\", \"4821\"]\nauthenticated = False\nlocked_out = False\n\nidx = 0\nmax_attempts = 3\n\nwhile idx < len(attempts) and idx < max_attempts:\n    if attempts[idx] == correct_pin:\n        authenticated = True\n        break\n    idx += 1\n\nif not authenticated:\n    locked_out = True\n\nprint(f\"Auth: {authenticated}, Locked: {locked_out}\")",
        "explanation": "The loop checks each attempt while tracking the attempt count up to `max_attempts`. If a matching PIN is found, `authenticated` is flagged and `break` terminates early. If all 3 attempts fail, `locked_out` is set to `True`.",
        "metadata": {
            "concept": "retry_and_lockout_system",
            "skill": "production_pattern",
            "learning_objective": "Build a real-world retry counter with early-exit and security lockout",
            "common_misconception": "Allowing attempts to exceed the security threshold",
            "why_this_exercise_exists": "Replaces generic mastery prompt with an authentic authentication challenge"
        }
    },

    # 6.7 Nested Loops
    "6.7_q2": {
        "id": "6.7_q2",
        "type": "output_prediction",
        "concept": "nested_loops_basics",
        "skill": "mental_model",
        "difficulty": "easy",
        "prerequisites": ["6.7_q1"],
        "prompt": "Predict the output of the following nested loop:\n\n```python\nfor row in range(2):\n    for col in range(3):\n        print(f\"({row},{col})\", end=\" \")\n    print()\n```",
        "options": [
            "(0,0) (0,1) (0,2) \n(1,0) (1,1) (1,2) ",
            "(0,0) (1,0) \n(0,1) (1,1) \n(0,2) (1,2) ",
            "(0,0) (0,1) (1,0) (1,1)",
            "(2,3)"
        ],
        "correct_answer": "(0,0) (0,1) (0,2) \n(1,0) (1,1) (1,2) ",
        "explanation": "For each iteration of the outer loop (`row = 0`, then `row = 1`), the inner loop runs completely through `col = 0, 1, 2`. This generates a 2D coordinate grid.",
        "metadata": {
            "concept": "nested_loop_execution_order",
            "skill": "tracing",
            "learning_objective": "Trace nested loop row-column execution ordering",
            "common_misconception": "Thinking outer and inner loops step in lockstep",
            "why_this_exercise_exists": "Replaces synthetic template function with coordinate grid iteration"
        }
    },
    "6.7_q4": {
        "id": "6.7_q4",
        "type": "code_prediction",
        "concept": "nested_loops_basics",
        "skill": "tracing",
        "difficulty": "medium",
        "prerequisites": ["6.7_q3"],
        "prompt": "How many times does the `count += 1` statement execute in this block?\n\n```python\ncount = 0\nfor i in range(4):\n    for j in range(3):\n        count += 1\nprint(count)\n```",
        "options": [
            "12",
            "7",
            "4",
            "3"
        ],
        "correct_answer": "12",
        "explanation": "The outer loop runs 4 times. For each outer iteration, the inner loop runs 3 times. Total executions = 4 * 3 = 12.",
        "metadata": {
            "concept": "nested_iteration_multiplication",
            "skill": "complexity_awareness",
            "learning_objective": "Calculate total iterations of nested independent loops",
            "common_misconception": "Adding loop iterations (4 + 3) instead of multiplying",
            "why_this_exercise_exists": "Replaces template function with iteration counting essential for Big-O analysis"
        }
    },
    "6.7_q5": {
        "id": "6.7_q5",
        "type": "output_prediction",
        "concept": "nested_loops_basics",
        "skill": "matrix_processing",
        "difficulty": "medium",
        "prerequisites": ["6.7_q4"],
        "prompt": "Trace this 2D matrix sum:\n\n```python\nmatrix = [\n    [1, 2],\n    [3, 4]\n]\ntotal = 0\nfor row in matrix:\n    for val in row:\n        total += val\nprint(total)\n```",
        "options": [
            "10",
            "7",
            "4",
            "14"
        ],
        "correct_answer": "10",
        "explanation": "The outer loop iterates over each row (`[1, 2]`, then `[3, 4]`). The inner loop extracts each number. 1 + 2 + 3 + 4 = 10.",
        "metadata": {
            "concept": "matrix_nested_iteration",
            "skill": "data_structures",
            "learning_objective": "Iterate through 2D nested lists to aggregate values",
            "common_misconception": "Summing whole sublists directly without inner iteration",
            "why_this_exercise_exists": "Replaces template function with realistic 2D data processing"
        }
    },
    "6.7_q6": {
        "id": "6.7_q6",
        "type": "fix_the_code",
        "concept": "nested_loops_basics",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["6.7_q5"],
        "prompt": "Fix the following code so that it prints a right triangle pattern of asterisks with heights 1 through 3:\n\n```python\n# Desired output:\n# *\n# **\n# ***\nfor i in range(1, 4):\n    # Fix line below so it prints i asterisks:\n    for j in range(1):\n        print(\"*\" * i)\n        break\n```",
        "starter_code": "for i in range(1, 4):\n    for j in range(1):\n        print(\"*\" * i)\n        break",
        "solution_code": "for i in range(1, 4):\n    row = \"\"\n    for j in range(i):\n        row += \"*\"\n    print(row)",
        "explanation": "Inner loop `range(i)` runs `i` times for each row `i` (1, then 2, then 3), accumulating `*` into `row` before printing.",
        "metadata": {
            "concept": "dependent_nested_loops",
            "skill": "pattern_generation",
            "learning_objective": "Implement nested loops where the inner range depends on the outer loop variable",
            "common_misconception": "Using fixed ranges for inner loops when triangle shapes require variable bounds",
            "why_this_exercise_exists": "Replaces template function with dependent loop iteration"
        }
    },
    "6.7_q10": {
        "id": "6.7_q10",
        "type": "write_the_code",
        "concept": "nested_loops_basics",
        "skill": "implementation",
        "difficulty": "medium",
        "prerequisites": ["6.7_q9"],
        "prompt": "Write a nested loop to flatten a 2D list `grid = [[10, 20], [30, 40]]` into a 1D list called `flat` containing `[10, 20, 30, 40]`.",
        "starter_code": "grid = [[10, 20], [30, 40]]\nflat = []\n# Iterate and append elements to flat\n",
        "solution_code": "grid = [[10, 20], [30, 40]]\nflat = []\nfor sublist in grid:\n    for item in sublist:\n        flat.append(item)\nprint(flat)",
        "explanation": "Iterating over each sublist and then over each element inside it appends items one by one into the flat 1D list.",
        "metadata": {
            "concept": "matrix_flattening",
            "skill": "data_manipulation",
            "learning_objective": "Flatten multi-dimensional lists into 1D sequences using nested loops",
            "common_misconception": "Appending sublists directly resulting in nested structures",
            "why_this_exercise_exists": "Replaces template function with an essential data transformation routine"
        }
    },

    # ==========================================
    # UNIT 7: STRINGS
    # ==========================================
    # 7.9 Project: String Formatter
    "7.9_q3": {
        "id": "7.9_q3",
        "type": "code_prediction",
        "concept": "project_string_formatter_titlecase",
        "skill": "string_methods",
        "difficulty": "medium",
        "prerequisites": ["7.9_q2"],
        "prompt": "What does `.title()` do when formatting a messy user name `\"ALICE smith-jones\"`?\n\n```python\nraw = \"ALICE smith-jones\"\nformatted = raw.title()\nprint(formatted)\n```",
        "options": [
            "Alice Smith-Jones",
            "ALICE SMITH-JONES",
            "Alice smith-jones",
            "Alice Smith-jones"
        ],
        "correct_answer": "Alice Smith-Jones",
        "explanation": "`title()` capitalizes the first character of each word (including words delimited by hyphens or spaces) and lowercases the remaining letters, yielding `'Alice Smith-Jones'`.",
        "metadata": {
            "concept": "title_case_normalization",
            "skill": "string_transformation",
            "learning_objective": "Apply title() for person and title capitalization",
            "common_misconception": "Expecting title() to ignore hyphenated words",
            "why_this_exercise_exists": "Replaces template function with real string formatter logic"
        }
    },
    "7.9_q4": {
        "id": "7.9_q4",
        "type": "error_diagnosis",
        "concept": "project_string_formatter_immutability",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["7.9_q3"],
        "prompt": "Why does `text` remain unchanged after calling `.strip()` in the snippet below?\n\n```python\ntext = \"  hello world  \"\ntext.strip()\nprint(f\"[{text}]\")\n```",
        "options": [
            "Strings in Python are immutable; methods return a new string rather than modifying in-place.",
            "strip() only removes trailing whitespace.",
            "print() re-adds whitespace automatically.",
            "SyntaxError: strip() must take arguments."
        ],
        "correct_answer": "Strings in Python are immutable; methods return a new string rather than modifying in-place.",
        "explanation": "Strings in Python cannot be mutated in place. Methods like `.strip()`, `.upper()`, and `.replace()` return *new* strings. To keep the result, you must reassign: `text = text.strip()`.",
        "metadata": {
            "concept": "string_immutability",
            "skill": "mental_model",
            "learning_objective": "Understand that string transformations produce new objects and require reassignment",
            "common_misconception": "Expecting string methods to mutate strings in-place like list methods do",
            "why_this_exercise_exists": "Replaces template function with one of Python's most fundamental string concepts"
        }
    },
    "7.9_q13": {
        "id": "7.9_q13",
        "type": "write_the_code",
        "concept": "project_string_formatter_milestone_1",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q12"],
        "prompt": "Formatter Milestone 1: Normalize a raw name input `raw_name = '  johnathan doe  '` by stripping leading/trailing whitespace and storing the cleaned string in `clean_name`.",
        "starter_code": "raw_name = \"  johnathan doe  \"\n# Strip whitespace and store in clean_name\n",
        "solution_code": "raw_name = \"  johnathan doe  \"\nclean_name = raw_name.strip()\nprint(f\"[{clean_name}]\")",
        "explanation": "Calling `.strip()` strips excess spaces from both ends of the string.",
        "metadata": {
            "concept": "name_normalization_stripping",
            "skill": "implementation",
            "learning_objective": "Clean extraneous whitespace from user names",
            "common_misconception": "Forgetting that strip() returns a new string",
            "why_this_exercise_exists": "Replaces milestone 1 with authentic formatter milestone 1"
        }
    },
    "7.9_q14": {
        "id": "7.9_q14",
        "type": "write_the_code",
        "concept": "project_string_formatter_milestone_2",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q13"],
        "prompt": "Formatter Milestone 2: Given `name = 'sarah connor'`, convert it to proper Title Case so that both first and last names start with a capital letter. Store the result in `formatted_name`.",
        "starter_code": "name = \"sarah connor\"\n# Capitalize properly and store in formatted_name\n",
        "solution_code": "name = \"sarah connor\"\nformatted_name = name.title()\nprint(formatted_name)",
        "explanation": "Calling `name.title()` capitalizes the first letter of each word, resulting in `'Sarah Connor'`.",
        "metadata": {
            "concept": "title_case_capitalization",
            "skill": "implementation",
            "learning_objective": "Capitalize multi-word names into standard Title Case",
            "common_misconception": "Using capitalize() which only capitalizes the very first letter of the entire string",
            "why_this_exercise_exists": "Replaces milestone 2 with authentic formatter milestone 2"
        }
    },
    "7.9_q15": {
        "id": "7.9_q15",
        "type": "write_the_code",
        "concept": "project_string_formatter_milestone_3",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q14"],
        "prompt": "Formatter Milestone 3: Given `first = 'ada'` and `last = 'lovelace'`, format them into a single string using an f-string with the format `'Lovelace, Ada'`. Store in `catalog_entry`.",
        "starter_code": "first = \"ada\"\nlast = \"lovelace\"\n# Format into 'Last, First' title-cased\n",
        "solution_code": "first = \"ada\"\nlast = \"lovelace\"\ncatalog_entry = f\"{last.capitalize()}, {first.capitalize()}\"\nprint(catalog_entry)",
        "explanation": "Using `f\"{last.capitalize()}, {first.capitalize()}\"` constructs `'Lovelace, Ada'` cleanly.",
        "metadata": {
            "concept": "fstring_composition",
            "skill": "implementation",
            "learning_objective": "Compose professional catalog names using f-strings and formatting methods",
            "common_misconception": "Concatenating with + and risking missing separators",
            "why_this_exercise_exists": "Replaces milestone 3 with authentic formatter milestone 3"
        }
    },
    "7.9_q16": {
        "id": "7.9_q16",
        "type": "write_the_code",
        "concept": "project_string_formatter_milestone_4",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q15"],
        "prompt": "Formatter Milestone 4: Format an address. Given `street = '742 evergreen terrace'`, `city = 'springfield'`, and `zip_code = '97477'`, assemble them into a standard address block `'742 Evergreen Terrace, Springfield, OR 97477'` assuming state `'OR'`. Store in `address_label`.",
        "starter_code": "street = \"742 evergreen terrace\"\ncity = \"springfield\"\nzip_code = \"97477\"\nstate = \"OR\"\n# Build formatted address_label\n",
        "solution_code": "street = \"742 evergreen terrace\"\ncity = \"springfield\"\nzip_code = \"97477\"\nstate = \"OR\"\naddress_label = f\"{street.title()}, {city.title()}, {state} {zip_code}\"\nprint(address_label)",
        "explanation": "Combining `.title()` on street and city with uppercase state and zip produces `'742 Evergreen Terrace, Springfield, OR 97477'`.",
        "metadata": {
            "concept": "address_formatting",
            "skill": "implementation",
            "learning_objective": "Format complex real-world addresses with multiple fields",
            "common_misconception": "Applying title() to state codes turning OR into Or",
            "why_this_exercise_exists": "Replaces milestone 4 with authentic formatter milestone 4"
        }
    },
    "7.9_q17": {
        "id": "7.9_q17",
        "type": "write_the_code",
        "concept": "project_string_formatter_milestone_5",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q16"],
        "prompt": "Formatter Milestone 5: Format a date string. Given `year = '2026'`, `month = '4'`, and `day = '7'`, zero-pad the month and day so they are 2 digits wide (`'04'` and `'07'`), and assemble into ISO format `'YYYY-MM-DD'`. Store in `iso_date`.",
        "starter_code": "year = \"2026\"\nmonth = \"4\"\nday = \"7\"\n# Pad and assemble into iso_date '2026-04-07'\n",
        "solution_code": "year = \"2026\"\nmonth = \"4\"\nday = \"7\"\niso_date = f\"{year}-{month.zfill(2)}-{day.zfill(2)}\"\nprint(iso_date)",
        "explanation": "Using `.zfill(2)` pads numeric strings with leading zeros to achieve a width of 2, producing `'2026-04-07'`.",
        "metadata": {
            "concept": "zero_padding_numeric_strings",
            "skill": "string_formatting",
            "learning_objective": "Format dates using zfill() or width specifiers",
            "common_misconception": "Manually appending '0' with an if statement",
            "why_this_exercise_exists": "Replaces milestone 5 with authentic formatter milestone 5"
        }
    },
    "7.9_q18": {
        "id": "7.9_q18",
        "type": "write_the_code",
        "concept": "project_string_formatter_milestone_6",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q17"],
        "prompt": "Formatter Milestone 6: Handle missing or empty optional fields. Given `unit_number = '   '`, check if `unit_number.strip()` is empty. If empty, set `unit_str = 'N/A'`; otherwise format as `f'Apt {unit_number.strip()}'`.",
        "starter_code": "unit_number = \"   \"\n# Handle missing or empty field\n",
        "solution_code": "unit_number = \"   \"\ncleaned = unit_number.strip()\nunit_str = f\"Apt {cleaned}\" if cleaned else \"N/A\"\nprint(unit_str)",
        "explanation": "If `cleaned` is empty `\"\"`, it evaluates as falsy, triggering the fallback `'N/A'`. This prevents trailing spaces or empty labels.",
        "metadata": {
            "concept": "fallback_string_handling",
            "skill": "sanitization",
            "learning_objective": "Provide robust defaults for empty or whitespace-only inputs",
            "common_misconception": "Treating whitespace '   ' as non-empty without stripping first",
            "why_this_exercise_exists": "Replaces milestone 6 with authentic formatter milestone 6"
        }
    },

    # ==========================================
    # UNIT 11: FUNCTIONS
    # ==========================================
    # 11.3 Parameters and Arguments
    "11.3_q25": {
        "id": "11.3_q25",
        "type": "error_diagnosis",
        "concept": "parameters_and_arguments_mismatch",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["11.3_q24"],
        "prompt": "Examine this function call:\n\n```python\ndef greet(name, age):\n    print(f\"Hello {name}, you are {age} years old\")\n\ngreet(\"Ganesh\")\n```\n\nWhat error occurs when this code runs and why?",
        "options": [
            "TypeError: greet() missing 1 required positional argument: 'age'",
            "ValueError: expected 2 arguments, received 1",
            "NameError: name 'age' is not defined",
            "SyntaxError: invalid argument count"
        ],
        "correct_answer": "TypeError: greet() missing 1 required positional argument: 'age'",
        "explanation": "In Python, parameters defined without default values are required positional arguments. If a caller fails to pass an argument for every required parameter, Python raises a `TypeError` indicating exactly which argument was missing.",
        "metadata": {
            "concept": "positional_arguments_contract",
            "skill": "error_diagnosis",
            "learning_objective": "Diagnose missing positional argument TypeErrors",
            "common_misconception": "Assuming unsupplied arguments automatically default to None",
            "why_this_exercise_exists": "Replaces template function with authentic parameter/argument validation"
        }
    },

    # 11.4 Returning Values
    "11.4_q28": {
        "id": "11.4_q28",
        "type": "output_prediction",
        "concept": "returning_values_print_vs_return",
        "skill": "mental_model",
        "difficulty": "medium",
        "prerequisites": ["11.4_q27"],
        "prompt": "A critical distinction in programming is `print()` versus `return`. What does this code print?\n\n```python\ndef square(n):\n    print(n * n)\n\nresult = square(4)\nprint(f\"Result is: {result}\")\n```",
        "options": [
            "16\nResult is: None",
            "16\nResult is: 16",
            "Result is: 16",
            "TypeError: cannot format NoneType"
        ],
        "correct_answer": "16\nResult is: None",
        "explanation": "Calling `square(4)` prints `16` to the console as a side-effect, but because `square()` does not have a `return` statement, it implicitly returns `None`. Therefore, `result` holds `None`!",
        "metadata": {
            "concept": "print_vs_return_distinction",
            "skill": "mental_model",
            "learning_objective": "Distinguish between printing to stdout and returning data to callers",
            "common_misconception": "Assuming print() returns the value it displays",
            "why_this_exercise_exists": "Fixes one of the deepest misconceptions in introductory programming"
        }
    },

    # 11.5 Multiple Parameters and Returns
    "11.5_q1": {
        "id": "11.5_q1",
        "type": "code_prediction",
        "concept": "multiple_parameters_and_returns_basics",
        "skill": "tuple_unpacking",
        "difficulty": "easy",
        "prerequisites": [],
        "prompt": "When a Python function returns multiple comma-separated values, what data structure does it actually return?\n\n```python\ndef get_dimensions():\n    width = 1920\n    height = 1080\n    return width, height\n\nres = get_dimensions()\nprint(type(res))\n```",
        "options": [
            "<class 'tuple'>",
            "<class 'list'>",
            "<class 'dict'>",
            "<class 'int'>"
        ],
        "correct_answer": "<class 'tuple'>",
        "explanation": "Returning multiple items separated by commas packs them into a single `tuple` object. Python automatically packages `return x, y` as `return (x, y)`.",
        "metadata": {
            "concept": "multiple_return_tuple_packing",
            "skill": "mental_model",
            "learning_objective": "Understand that multiple return values are packed into a tuple",
            "common_misconception": "Believing Python returns multiple independent return values simultaneously",
            "why_this_exercise_exists": "Replaces template function with core tuple-packing mechanics"
        }
    },
    "11.5_q13": {
        "id": "11.5_q13",
        "type": "output_prediction",
        "concept": "multiple_parameters_and_returns_unpacking",
        "skill": "tracing",
        "difficulty": "medium",
        "prerequisites": ["11.5_q12"],
        "prompt": "Trace the execution of this score analysis function:\n\n```python\ndef analyze_scores(scores):\n    return min(scores), max(scores), sum(scores) / len(scores)\n\nlowest, highest, average = analyze_scores([80, 90, 100])\nprint(f\"{lowest}-{highest} (avg: {average:.0f})\")\n```\n\nWhat is output?",
        "options": [
            "80-100 (avg: 90)",
            "100-80 (avg: 90)",
            "80-100 (avg: 90.0)",
            "TypeError: cannot unpack tuple"
        ],
        "correct_answer": "80-100 (avg: 90)",
        "explanation": "`analyze_scores` returns `(80, 100, 90.0)`. Unpacking assigns `lowest = 80`, `highest = 100`, and `average = 90.0`. Format specifier `:.0f` displays `90`.",
        "metadata": {
            "concept": "multi_return_unpacking_analytics",
            "skill": "implementation",
            "learning_objective": "Unpack multiple function returns into descriptive variables",
            "common_misconception": "Mismatched unpacking variable count",
            "why_this_exercise_exists": "Replaces template function with authentic multi-value statistical reporting"
        }
    },
    "11.5_q25": {
        "id": "11.5_q25",
        "type": "write_the_code",
        "concept": "multiple_parameters_and_returns_construction",
        "skill": "construction",
        "difficulty": "hard",
        "prerequisites": ["11.5_q24"],
        "prompt": "Write a function `min_max_sum(numbers)` that takes a list of integers and returns a tuple of 3 elements: `(minimum, maximum, total_sum)`. Call it with `[5, 12, 3]` and unpack into `low, high, total`.",
        "starter_code": "def min_max_sum(numbers):\n    # Return min, max, and sum\n    pass\n\nlow, high, total = min_max_sum([5, 12, 3])\nprint(low, high, total)",
        "solution_code": "def min_max_sum(numbers):\n    return min(numbers), max(numbers), sum(numbers)\n\nlow, high, total = min_max_sum([5, 12, 3])\nprint(low, high, total)",
        "explanation": "`min([5, 12, 3])` is 3, `max` is 12, and `sum` is 20. Returning them together creates a 3-tuple `(3, 12, 20)` which is cleanly unpacked.",
        "metadata": {
            "concept": "multi_value_return_implementation",
            "skill": "function_design",
            "learning_objective": "Design and consume functions returning multiple coordinated outputs",
            "common_misconception": "Returning a list when an immutable tuple is standard",
            "why_this_exercise_exists": "Replaces template function with practical aggregate analysis"
        }
    },

    # ==========================================
    # UNIT 12: ERRORS AND DEBUGGING
    # ==========================================
    # 12.1 Syntax Errors vs Runtime Errors
    "12.1_q2": {
        "id": "12.1_q2",
        "type": "error_diagnosis",
        "concept": "syntax_errors_vs_runtime_errors_basics",
        "skill": "error_discrimination",
        "difficulty": "easy",
        "prerequisites": ["12.1_q1"],
        "prompt": "Consider the following line of code:\n\n```python\nif age > 18\n    print(\"Adult\")\n```\n\nWhat category of error does this represent?",
        "options": [
            "SyntaxError: invalid syntax (caught at parse time before any code runs)",
            "RuntimeError: occurs while the program is actively executing",
            "Logical Error: the program runs to completion but gives wrong answers",
            "TypeError: incompatible data types"
        ],
        "correct_answer": "SyntaxError: invalid syntax (caught at parse time before any code runs)",
        "explanation": "A missing colon `:` violates Python's formal grammatical rules. Python's parser detects this during compilation/parsing *before* executing even a single line of code, raising a `SyntaxError`.",
        "metadata": {
            "concept": "parse_time_syntax_error",
            "skill": "error_classification",
            "learning_objective": "Distinguish compile/parse-time SyntaxErrors from runtime exceptions",
            "common_misconception": "Thinking Python executes lines up until the line with missing colon",
            "why_this_exercise_exists": "Replaces template function with core compiler/interpreter mental model"
        }
    },
    "12.1_q4": {
        "id": "12.1_q4",
        "type": "error_diagnosis",
        "concept": "syntax_errors_vs_runtime_errors_basics",
        "skill": "error_discrimination",
        "difficulty": "medium",
        "prerequisites": ["12.1_q3"],
        "prompt": "Consider this code where `user_name` has not been initialized:\n\n```python\nprint(\"Welcome to our app!\")\nprint(user_name)\n```\n\nDoes Python print the welcome message before crashing?",
        "options": [
            "Yes; 'Welcome to our app!' prints first, then Python raises NameError at runtime on line 2.",
            "No; Python crashes with SyntaxError before printing anything.",
            "Yes; user_name defaults to None so no crash occurs.",
            "No; Python does not support printing undefined variables."
        ],
        "correct_answer": "Yes; 'Welcome to our app!' prints first, then Python raises NameError at runtime on line 2.",
        "explanation": "Because the code is syntactically valid, Python compiles it and begins execution. Line 1 runs successfully, printing the welcome string. When line 2 attempts to evaluate the undefined variable `user_name`, execution halts with a runtime `NameError`.",
        "metadata": {
            "concept": "runtime_exception_timing",
            "skill": "tracing",
            "learning_objective": "Understand that runtime errors occur during execution, after valid parsing",
            "common_misconception": "Assuming runtime errors prevent prior valid statements from executing",
            "why_this_exercise_exists": "Replaces template function with essential execution lifecycle understanding"
        }
    },
    "12.1_q5": {
        "id": "12.1_q5",
        "type": "code_prediction",
        "concept": "syntax_errors_vs_runtime_errors_basics",
        "skill": "error_discrimination",
        "difficulty": "medium",
        "prerequisites": ["12.1_q4"],
        "prompt": "Which of the following mistakes will prevent the ENTIRE script from even starting execution?",
        "options": [
            "def calculate(x, y)  # Missing colon",
            "result = 10 / 0      # ZeroDivisionError",
            "items = [1, 2][5]     # IndexError",
            "data = int(\"abc\")     # ValueError"
        ],
        "correct_answer": "def calculate(x, y)  # Missing colon",
        "explanation": "The missing colon in `def calculate(x, y)` is a `SyntaxError`. Python checks grammar for the entire file before running; syntax errors stop execution completely before line 1 runs. The other options are runtime errors that only trigger when the interpreter reaches them.",
        "metadata": {
            "concept": "syntax_error_precedence",
            "skill": "classification",
            "learning_objective": "Identify errors that halt execution before runtime",
            "common_misconception": "Treating all errors as runtime exceptions",
            "why_this_exercise_exists": "Replaces template function with rigorous syntactic comprehension"
        }
    },
    "12.1_q6": {
        "id": "12.1_q6",
        "type": "fix_the_code",
        "concept": "syntax_errors_vs_runtime_errors_basics",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["12.1_q5"],
        "prompt": "The code below contains both a SyntaxError and a potential runtime TypeError. Fix both issues so it successfully prints `Double 10 is 20`:\n\n```python\n# Fix syntax and type conversion:\nval = \"10\"\nif val.isdigit()\n    print(f\"Double {val} is {val * 2}\")\n```",
        "starter_code": "val = \"10\"\nif val.isdigit()\n    print(f\"Double {val} is {val * 2}\")",
        "solution_code": "val = \"10\"\nif val.isdigit():\n    num = int(val)\n    print(f\"Double {val} is {num * 2}\")",
        "explanation": "1. Added the missing colon `:` after `if val.isdigit()`. 2. Converted `val` to `int(val)` so `num * 2` performs mathematical multiplication (`20`) rather than string duplication (`'1010'`).",
        "metadata": {
            "concept": "syntax_and_semantic_repair",
            "skill": "repair",
            "learning_objective": "Repair parse-time syntax and runtime type mismatches in a single pass",
            "common_misconception": "Thinking val * 2 doubles the numeric value when val is a string",
            "why_this_exercise_exists": "Replaces template function with dual-stage debugging"
        }
    },
    "12.5_q19": {
        "id": "12.5_q19",
        "type": "fix_the_code",
        "concept": "debugging_strategies_trace",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["12.5_q18"],
        "prompt": "A developer is debugging a calculation bug where an average score is computed incorrectly due to integer floor division. Fix the calculation so it yields the true floating-point average `87.5`.\n\n```python\nscores = [85, 90]\n# Fix calculation below:\navg = sum(scores) // len(scores)\nprint(avg)\n```",
        "starter_code": "scores = [85, 90]\navg = sum(scores) // len(scores)\nprint(avg)",
        "solution_code": "scores = [85, 90]\navg = sum(scores) / len(scores)\nprint(avg)",
        "explanation": "Floor division `//` discards decimal remainders, truncating `175 / 2 = 87.5` down to `87`. Using standard division `/` yields the exact float `87.5`.",
        "metadata": {
            "concept": "operator_precision_bug",
            "skill": "repair",
            "learning_objective": "Fix subtle logic bugs caused by unintended integer floor division",
            "common_misconception": "Confusing / with //",
            "why_this_exercise_exists": "Replaces template function with an authentic arithmetic precision fix"
        }
    },

    # ==========================================
    # UNIT 13: FILE HANDLING
    # ==========================================
    # 13.1 Reading Text Files
    "13.1_q2": {
        "id": "13.1_q2",
        "type": "output_prediction",
        "concept": "reading_text_files_basics",
        "skill": "file_io",
        "difficulty": "easy",
        "prerequisites": ["13.1_q1"],
        "prompt": "What does `.read()` return when executed on an open text file object?\n\n```python\n# Simulated file containing 'Hello\\nWorld'\nwith open(\"sample.txt\", \"r\") as f:\n    content = f.read()\nprint(type(content))\n```",
        "options": [
            "<class 'str'>",
            "<class 'list'>",
            "<class 'bytes'>",
            "<class 'dict'>"
        ],
        "correct_answer": "<class 'str'>",
        "explanation": "Calling `file.read()` reads the entire contents of a text file from the current pointer to the end of the file as a single string (`str`). To get a list of lines, you would use `.readlines()`.",
        "metadata": {
            "concept": "file_read_return_type",
            "skill": "mental_model",
            "learning_objective": "Recognize that f.read() returns the entire file as a single string",
            "common_misconception": "Expecting read() to return a list of lines",
            "why_this_exercise_exists": "Replaces template function with foundational file I/O types"
        }
    },
    "13.1_q4": {
        "id": "13.1_q4",
        "type": "code_prediction",
        "concept": "reading_text_files_basics",
        "skill": "newline_stripping",
        "difficulty": "medium",
        "prerequisites": ["13.1_q3"],
        "prompt": "When iterating over a file line by line, why does `print(line)` often produce double blank lines in the terminal?\n\n```python\nwith open(\"data.txt\") as f:\n    for line in f:\n        print(line)\n```",
        "options": [
            "Each line in the file ends with '\\n', and print() automatically adds its own '\\n'.",
            "The file pointer skips every other line.",
            "open() doubles all whitespace automatically.",
            "print() only prints on even lines."
        ],
        "correct_answer": "Each line in the file ends with '\\n', and print() automatically adds its own '\\n'.",
        "explanation": "File lines keep their trailing newline character `'\\n'`. Because `print()` appends an additional newline by default, consecutive lines appear with blank lines between them. To fix this, use `line.strip()` or `print(line, end=\"\")`.",
        "metadata": {
            "concept": "file_line_trailing_newlines",
            "skill": "file_io",
            "learning_objective": "Understand and handle trailing newline characters when reading files",
            "common_misconception": "Assuming iterating over a file automatically strips newline characters",
            "why_this_exercise_exists": "Replaces template function with an essential CLI text processing concept"
        }
    },
    "13.1_q5": {
        "id": "13.1_q5",
        "type": "error_diagnosis",
        "concept": "reading_text_files_basics",
        "skill": "exception_handling",
        "difficulty": "medium",
        "prerequisites": ["13.1_q4"],
        "prompt": "What happens if you call `open(\"non_existent.txt\", \"r\")` for a file that does not exist on disk?",
        "options": [
            "FileNotFoundError: [Errno 2] No such file or directory",
            "Python creates an empty file automatically in 'r' mode",
            "Returns None without raising an exception",
            "ZeroDivisionError"
        ],
        "correct_answer": "FileNotFoundError: [Errno 2] No such file or directory",
        "explanation": "Opening a non-existent file in read mode (`'r'`) immediately raises a `FileNotFoundError`. Only write modes like `'w'` or `'a'` create the file if it does not already exist.",
        "metadata": {
            "concept": "filenotfound_exception",
            "skill": "error_recognition",
            "learning_objective": "Recognize FileNotFoundError when opening missing files for reading",
            "common_misconception": "Assuming read mode creates missing files automatically",
            "why_this_exercise_exists": "Replaces template function with defensive file system practices"
        }
    },
    "13.1_q6": {
        "id": "13.1_q6",
        "type": "fix_the_code",
        "concept": "reading_text_files_basics",
        "skill": "resource_management",
        "difficulty": "medium",
        "prerequisites": ["13.1_q5"],
        "prompt": "Refactor this legacy file reading code to use the modern, safe context manager (`with open(...)`) so the file is guaranteed to close even if an error occurs:\n\n```python\nf = open(\"config.txt\", \"r\")\ncontent = f.read()\nf.close()\n```",
        "starter_code": "f = open(\"config.txt\", \"r\")\ncontent = f.read()\nf.close()",
        "solution_code": "with open(\"config.txt\", \"r\") as f:\n    content = f.read()",
        "explanation": "Using `with open(...) as f:` creates a context manager that automatically guarantees the file descriptor is cleanly closed upon exiting the block, even if an exception is raised.",
        "metadata": {
            "concept": "context_manager_file_handling",
            "skill": "best_practices",
            "learning_objective": "Refactor manual close() calls to idiomatic with open() context managers",
            "common_misconception": "Relying on manual f.close() which leaks descriptors on exceptions",
            "why_this_exercise_exists": "Replaces template function with standard production file handling"
        }
    },

    # ==========================================
    # UNIT 14: CSV AND JSON
    # ==========================================
    # 14.1 Introduction to CSV
    "14.1_q26": {
        "id": "14.1_q26",
        "type": "code_prediction",
        "concept": "csv_dictreader_parsing",
        "skill": "data_parsing",
        "difficulty": "medium",
        "prerequisites": ["14.1_q25"],
        "prompt": "What data type does each row represent when read using `csv.DictReader`?\n\n```python\nimport csv\nfrom io import StringIO\n\ncsv_data = \"name,score\\nAlice,95\\nBob,88\"\nreader = csv.DictReader(StringIO(csv_data))\nrow = next(reader)\nprint(type(row))\nprint(row[\"name\"])\n```",
        "options": [
            "<class 'dict'> (or dict-like object)\nAlice",
            "<class 'list'>\nAlice",
            "<class 'tuple'>\nAlice",
            "<class 'str'>\nAlice"
        ],
        "correct_answer": "<class 'dict'> (or dict-like object)\nAlice",
        "explanation": "`csv.DictReader` maps each data row to a dictionary where keys are the column headers defined in the first row. Thus `row[\"name\"]` accesses `'Alice'` directly.",
        "metadata": {
            "concept": "csv_dictreader_structure",
            "skill": "data_structures",
            "learning_objective": "Parse structured CSV lines into key-value dictionaries",
            "common_misconception": "Assuming csv reader only returns index-based lists",
            "why_this_exercise_exists": "Replaces template function with practical tabular data ingestion"
        }
    },

    # 14.5 Generating JSON
    "14.5_q2": {
        "id": "14.5_q2",
        "type": "output_prediction",
        "concept": "generating_json_basics",
        "skill": "serialization",
        "difficulty": "easy",
        "prerequisites": ["14.5_q1"],
        "prompt": "What does `json.dumps()` return when serializing a Python dictionary?\n\n```python\nimport json\n\nuser = {\"id\": 101, \"active\": True}\npayload = json.dumps(user)\nprint(type(payload))\nprint(payload)\n```",
        "options": [
            "<class 'str'>\n{\"id\": 101, \"active\": true}",
            "<class 'dict'>\n{\"id\": 101, \"active\": True}",
            "<class 'bytes'>\n{\"id\": 101, \"active\": true}",
            "<class 'str'>\n{\"id\": 101, \"active\": True}"
        ],
        "correct_answer": "<class 'str'>\n{\"id\": 101, \"active\": true}",
        "explanation": "`json.dumps()` (dump to string) returns a `str`. Notice that Python's boolean `True` is serialized to lowercase JSON boolean `true` according to the JSON specification.",
        "metadata": {
            "concept": "json_dumps_string_serialization",
            "skill": "type_conversion",
            "learning_objective": "Recognize that json.dumps() produces a serialized string and maps True to true",
            "common_misconception": "Confusing Python's True with JSON's lowercase true",
            "why_this_exercise_exists": "Replaces template function with exact JSON specification behavior"
        }
    },
    "14.5_q4": {
        "id": "14.5_q4",
        "type": "code_prediction",
        "concept": "generating_json_basics",
        "skill": "api_discrimination",
        "difficulty": "medium",
        "prerequisites": ["14.5_q3"],
        "prompt": "What is the critical difference between `json.dump()` and `json.dumps()` in Python?",
        "options": [
            "json.dump() writes to a file-like stream; json.dumps() returns a Python string.",
            "json.dump() is for lists; json.dumps() is for dictionaries.",
            "json.dumps() writes directly to a database.",
            "There is no difference; they are aliases."
        ],
        "correct_answer": "json.dump() writes to a file-like stream; json.dumps() returns a Python string.",
        "explanation": "The 's' in `dumps` stands for 'string'. `json.dumps(obj)` serializes `obj` and returns a string in memory. `json.dump(obj, file_handle)` serializes `obj` directly into a writable file stream.",
        "metadata": {
            "concept": "dump_vs_dumps_distinction",
            "skill": "api_knowledge",
            "learning_objective": "Discriminate between file-stream serialization (dump) and string serialization (dumps)",
            "common_misconception": "Attempting to pass a file object to json.dumps()",
            "why_this_exercise_exists": "Replaces template function with essential API distinction"
        }
    },
    "14.5_q5": {
        "id": "14.5_q5",
        "type": "error_diagnosis",
        "concept": "generating_json_basics",
        "skill": "serialization_limits",
        "difficulty": "medium",
        "prerequisites": ["14.5_q4"],
        "prompt": "What happens if you attempt to serialize a Python `set` using `json.dumps()` without a custom serializer?\n\n```python\nimport json\ndata = {\"tags\": {\"python\", \"coding\"}}\njson.dumps(data)\n```",
        "options": [
            "TypeError: Object of type set is not JSON serializable",
            "Serializes the set to a JSON array automatically",
            "Ignores the set and outputs {\"tags\": null}",
            "Converts the set to a comma-separated string"
        ],
        "correct_answer": "TypeError: Object of type set is not JSON serializable",
        "explanation": "Standard JSON format only supports strings, numbers, booleans, null, arrays (lists), and objects (dicts). It has no native representation for `set`, `datetime`, or custom classes. Attempting to serialize a `set` raises a `TypeError`.",
        "metadata": {
            "concept": "json_serializability_constraints",
            "skill": "error_recognition",
            "learning_objective": "Identify types that are not natively serializable to JSON (like sets)",
            "common_misconception": "Assuming sets serialize automatically as JSON arrays",
            "why_this_exercise_exists": "Replaces template function with realistic serialization debugging"
        }
    },
    "14.5_q6": {
        "id": "14.5_q6",
        "type": "write_the_code",
        "concept": "generating_json_basics",
        "skill": "pretty_printing",
        "difficulty": "medium",
        "prerequisites": ["14.5_q5"],
        "prompt": "Write a snippet using `json.dumps()` that formats the dictionary `config = {'app': 'codolingo', 'version': 2}` with an indentation of 2 spaces so it produces readable, indented JSON.",
        "starter_code": "import json\nconfig = {\"app\": \"codolingo\", \"version\": 2}\n# Format with 2-space indentation\n",
        "solution_code": "import json\nconfig = {\"app\": \"codolingo\", \"version\": 2}\npretty_json = json.dumps(config, indent=2)\nprint(pretty_json)",
        "explanation": "Passing `indent=2` to `json.dumps()` instructs the serializer to pretty-print the JSON structure with 2 spaces of indentation per level.",
        "metadata": {
            "concept": "json_indentation_pretty_printing",
            "skill": "implementation",
            "learning_objective": "Format JSON strings for human readability using the indent parameter",
            "common_misconception": "Manually adding newlines and spaces to JSON strings",
            "why_this_exercise_exists": "Replaces template function with standard logging and configuration formatting"
        }
    },
    "14.6_q10": {
        "id": "14.6_q10",
        "type": "write_the_code",
        "concept": "project_cli_expense_tracker_total",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["14.6_q9"],
        "prompt": "Expense Tracker Milestone: Given a list of expense records `expenses = [{'category': 'Food', 'amount': 15.50}, {'category': 'Transport', 'amount': 4.50}, {'category': 'Food', 'amount': 12.00}]`, compute the total spending in the `'Food'` category.",
        "starter_code": "expenses = [\n    {\"category\": \"Food\", \"amount\": 15.50},\n    {\"category\": \"Transport\", \"amount\": 4.50},\n    {\"category\": \"Food\", \"amount\": 12.00}\n]\nfood_total = 0.0\n# Sum amounts where category == 'Food'\n",
        "solution_code": "expenses = [\n    {\"category\": \"Food\", \"amount\": 15.50},\n    {\"category\": \"Transport\", \"amount\": 4.50},\n    {\"category\": \"Food\", \"amount\": 12.00}\n]\nfood_total = sum(e[\"amount\"] for e in expenses if e[\"category\"] == \"Food\")\nprint(f\"Food total: ${food_total:.2f}\")",
        "explanation": "Filtering with a generator expression `e[\"amount\"] for e in expenses if e[\"category\"] == \"Food\"` sums `15.50 + 12.00 = 27.50`.",
        "metadata": {
            "concept": "expense_filtering_aggregation",
            "skill": "data_analysis",
            "learning_objective": "Aggregate numeric fields by category in structured dictionary records",
            "common_misconception": "Summing all amounts without category filtering",
            "why_this_exercise_exists": "Replaces template function with core CLI expense tracker analytics"
        }
    }
}
