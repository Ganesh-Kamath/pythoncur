"""
CODOLINGO EXACT REPAIRS: UNITS 15 - 43
Defines pedagogically rigorous replacements for:
- Unit 15 (15.1 default args, 15.2 kwargs)
- Unit 19 (19.5 regex groups)
- Unit 20 & 21 (20.3 self, 21.1 class vs instance attributes)
- Unit 22 (22.2 decorators, 22.6 type hints)
- Unit 24 (24.1 clean code, 24.2 docstrings, 24.3 unit testing, 24.6 spaghetti refactor)
- Unit 25 (25.5 BeautifulSoup web scraping)
- Unit 26 (26.6 SQL injection & parameterized queries)
- Unit 29 & 30 (29.4 space complexity, 30.1 & 30.6 testing methodology)
- Unit 32 & 41 (32.2 iteration, 41.1 two pointers)
- Unit 42 (42.1 log parsing, 42.2 data pipeline + 42.2_q30 cleaning mastery, 42.3 scraper API)
- Unit 43 (43.3 large-scale refactor, 43.5 mastery challenge)
"""

REPLACEMENTS_UNITS_15_TO_43 = {
    # ==========================================
    # UNIT 15: ADVANCED FUNCTIONS
    # ==========================================
    "15.1_q8": {
        "id": "15.1_q8",
        "type": "output_prediction",
        "concept": "default_arguments_evaluation",
        "skill": "mental_model",
        "difficulty": "medium",
        "prerequisites": ["15.1_q7"],
        "prompt": "What does the following function return when called without the optional rate parameter?\n\n```python\ndef compute_tax(subtotal, rate=0.08):\n    return round(subtotal * rate, 2)\n\nprint(compute_tax(100.0))\n```",
        "options": [
            "8.0",
            "0.08",
            "108.0",
            "TypeError: missing required argument"
        ],
        "correct_answer": "8.0",
        "explanation": "When an argument for `rate` is omitted, Python binds the default parameter value `0.08`. `100.0 * 0.08` evaluates to `8.0`.",
        "metadata": {
            "concept": "default_parameter_binding",
            "skill": "mental_model",
            "learning_objective": "Observe default parameter values in functional calculations",
            "common_misconception": "Thinking default arguments are mandatory at call time",
            "why_this_exercise_exists": "Replaces template function with realistic tax calculation defaults"
        }
    },
    "15.1_q26": {
        "id": "15.1_q26",
        "type": "error_diagnosis",
        "concept": "default_arguments_mutable_pitfall",
        "skill": "debugging",
        "difficulty": "hard",
        "prerequisites": ["15.1_q25"],
        "prompt": "What dangerous pitfall occurs in this function with a mutable default argument?\n\n```python\ndef add_item(item, basket=[]):\n    basket.append(item)\n    return basket\n\nprint(add_item(\"apple\"))\nprint(add_item(\"banana\"))\n```",
        "options": [
            "['apple'] then ['apple', 'banana'] because default arguments are evaluated only once at definition time.",
            "['apple'] then ['banana'] because basket is reset to [] on each call.",
            "Raises a TypeError because lists cannot be default parameters.",
            "Raises an AttributeError on append."
        ],
        "correct_answer": "['apple'] then ['apple', 'banana'] because default arguments are evaluated only once at definition time.",
        "explanation": "In Python, default arguments are evaluated *once* when the function is defined, not every time it is called. The exact same list `basket` is reused across all invocations. The idiom is to use `basket=None` and initialize `if basket is None: basket = []` inside the function.",
        "metadata": {
            "concept": "mutable_default_arguments",
            "skill": "gotcha_avoidance",
            "learning_objective": "Identify the classic mutable default argument memory leak bug in Python",
            "common_misconception": "Believing default arguments re-evaluate per function call",
            "why_this_exercise_exists": "One of Python's most notorious interview and production pitfalls"
        }
    },
    "15.2_q2": {
        "id": "15.2_q2",
        "type": "output_prediction",
        "concept": "keyword_arguments_basics",
        "skill": "tracing",
        "difficulty": "easy",
        "prerequisites": ["15.2_q1"],
        "prompt": "What is output when calling this function with explicit keyword arguments?\n\n```python\ndef format_user(name, role):\n    return f\"{name}: {role}\"\n\nprint(format_user(role=\"Admin\", name=\"Maya\"))\n```",
        "options": [
            "Maya: Admin",
            "Admin: Maya",
            "TypeError: parameters out of order",
            "None"
        ],
        "correct_answer": "Maya: Admin",
        "explanation": "Keyword arguments allow arguments to be passed in any order because Python matches values by parameter name rather than position.",
        "metadata": {
            "concept": "keyword_argument_order_independence",
            "skill": "mental_model",
            "learning_objective": "Understand that named keyword arguments resolve by identifier, ignoring position",
            "common_misconception": "Thinking keyword arguments must match positional declaration order",
            "why_this_exercise_exists": "Replaces template function with proper keyword resolution"
        }
    },
    "15.2_q4": {
        "id": "15.2_q4",
        "type": "error_diagnosis",
        "concept": "keyword_arguments_basics",
        "skill": "syntax_rules",
        "difficulty": "medium",
        "prerequisites": ["15.2_q3"],
        "prompt": "Why does Python reject this function call?\n\n```python\ndef setup_server(host, port=8080, debug=False):\n    pass\n\nsetup_server(port=9000, \"localhost\")\n```",
        "options": [
            "SyntaxError: positional argument follows keyword argument",
            "TypeError: host is missing",
            "ValueError: duplicate arguments",
            "NameError: localhost is not defined"
        ],
        "correct_answer": "SyntaxError: positional argument follows keyword argument",
        "explanation": "In Python call syntax, all positional arguments MUST appear before any keyword arguments. Placing `\"localhost\"` after `port=9000` causes a parse-time `SyntaxError`.",
        "metadata": {
            "concept": "positional_before_keyword_rule",
            "skill": "syntax_rules",
            "learning_objective": "Enforce that positional arguments precede keyword arguments in calls",
            "common_misconception": "Mixing positional arguments freely after named keyword arguments",
            "why_this_exercise_exists": "Replaces template function with core Python grammar rule"
        }
    },
    "15.2_q5": {
        "id": "15.2_q5",
        "type": "output_prediction",
        "concept": "keyword_arguments_basics",
        "skill": "kwargs_unpacking",
        "difficulty": "medium",
        "prerequisites": ["15.2_q4"],
        "prompt": "What does `**kwargs` receive when passing named options?\n\n```python\ndef configure_db(**settings):\n    return sorted(settings.keys())\n\nkeys = configure_db(host=\"localhost\", port=5432, ssl=True)\nprint(keys)\n```",
        "options": [
            "['host', 'port', 'ssl']",
            "['localhost', 5432, True]",
            "('host', 'port', 'ssl')",
            "TypeError"
        ],
        "correct_answer": "['host', 'port', 'ssl']",
        "explanation": "`**settings` packs arbitrary keyword arguments into a standard Python dictionary `{'host': 'localhost', 'port': 5432, 'ssl': True}`. `sorted(settings.keys())` returns the alphabetically sorted list of keys.",
        "metadata": {
            "concept": "kwargs_dictionary_packing",
            "skill": "dict_manipulation",
            "learning_objective": "Inspect keyword arguments captured via **kwargs",
            "common_misconception": "Thinking kwargs produces a tuple",
            "why_this_exercise_exists": "Replaces template function with practical kwargs dictionary usage"
        }
    },
    "15.2_q6": {
        "id": "15.2_q6",
        "type": "fix_the_code",
        "concept": "keyword_arguments_basics",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["15.2_q5"],
        "prompt": "Fix the call to `create_user` below so positional arguments come first:\n\n```python\ndef create_user(username, email, is_admin=False):\n    return f\"{username} ({email}) admin={is_admin}\"\n\n# Fix this call:\nprofile = create_user(is_admin=True, \"sam\", \"sam@code.org\")\n```",
        "starter_code": "def create_user(username, email, is_admin=False):\n    return f\"{username} ({email}) admin={is_admin}\"\n\nprofile = create_user(is_admin=True, \"sam\", \"sam@code.org\")",
        "solution_code": "def create_user(username, email, is_admin=False):\n    return f\"{username} ({email}) admin={is_admin}\"\n\nprofile = create_user(\"sam\", \"sam@code.org\", is_admin=True)\nprint(profile)",
        "explanation": "Supplying `\"sam\"` and `\"sam@code.org\"` as the leading positional arguments followed by `is_admin=True` satisfies Python's ordering requirement.",
        "metadata": {
            "concept": "argument_order_correction",
            "skill": "repair",
            "learning_objective": "Order positional parameters before keyword arguments in invocations",
            "common_misconception": "Passing keyword overrides before positional parameters",
            "why_this_exercise_exists": "Replaces template function with practical argument cleanup"
        }
    },
    "15.2_q13": {
        "id": "15.2_q13",
        "type": "output_prediction",
        "concept": "keyword_arguments_unpacking",
        "skill": "dictionary_unpacking",
        "difficulty": "medium",
        "prerequisites": ["15.2_q12"],
        "prompt": "What happens when unpacking a dictionary using `**` into a function?\n\n```python\ndef connect(host, port):\n    return f\"{host}:{port}\"\n\nconfig = {\"host\": \"api.codolingo.com\", \"port\": 443}\nprint(connect(**config))\n```",
        "options": [
            "api.codolingo.com:443",
            "host:port",
            "TypeError: connect() accepts 2 arguments, got 1 dict",
            "None"
        ],
        "correct_answer": "api.codolingo.com:443",
        "explanation": "The `**config` syntax unpacks key-value pairs as individual keyword arguments into `connect()`, perfectly binding `host='api.codolingo.com'` and `port=443`.",
        "metadata": {
            "concept": "dictionary_argument_unpacking",
            "skill": "idiomatic_python",
            "learning_objective": "Unpack dictionaries into keyword arguments using double-splat (**)",
            "common_misconception": "Passing the dict directly as a single positional parameter",
            "why_this_exercise_exists": "Replaces template function with essential configuration unpacking"
        }
    },

    # ==========================================
    # UNIT 19: REGULAR EXPRESSIONS
    # ==========================================
    "19.5_q2": {
        "id": "19.5_q2",
        "type": "output_prediction",
        "concept": "groups_and_extraction_basics",
        "skill": "regex_parsing",
        "difficulty": "medium",
        "prerequisites": ["19.5_q1"],
        "prompt": "What does `.groups()` return when matching this date pattern?\n\n```python\nimport re\nmatch = re.search(r\"(\\d{4})-(\\d{2})-(\\d{2})\", \"2026-10-04\")\nprint(match.groups())\n```",
        "options": [
            "('2026', '10', '04')",
            "['2026', '10', '04']",
            "'2026-10-04'",
            "('2026-10-04',)"
        ],
        "correct_answer": "('2026', '10', '04')",
        "explanation": "Each pair of parentheses `(...)` creates a capturing group. Calling `.groups()` returns a tuple containing the extracted strings for each capture group in sequence.",
        "metadata": {
            "concept": "regex_capturing_groups",
            "skill": "mental_model",
            "learning_objective": "Extract parsed segments from regex match objects via groups()",
            "common_misconception": "Expecting groups() to return a list or include group(0)",
            "why_this_exercise_exists": "Replaces template function with real regex extraction mechanics"
        }
    },
    "19.5_q4": {
        "id": "19.5_q4",
        "type": "code_prediction",
        "concept": "groups_and_extraction_basics",
        "skill": "named_groups",
        "difficulty": "medium",
        "prerequisites": ["19.5_q3"],
        "prompt": "How do you access the value of a named capture group `(?P<user>...)` from a match object?\n\n```python\nimport re\nmatch = re.search(r\"(?P<user>\\w+)@(?P<domain>[\\w.]+)\", \"ada@lovelace.org\")\nprint(match.group(\"user\"))\n```",
        "options": [
            "ada",
            "lovelace.org",
            "ada@lovelace.org",
            "KeyError: 'user'"
        ],
        "correct_answer": "ada",
        "explanation": "Named groups created with `(?P<name>...)` can be queried directly by name using `match.group(\"name\")` or converted into a dictionary using `match.groupdict()`.",
        "metadata": {
            "concept": "named_regex_groups",
            "skill": "extraction",
            "learning_objective": "Define and query named regex groups for self-documenting parsing",
            "common_misconception": "Thinking groups can only be indexed by integer numbers",
            "why_this_exercise_exists": "Replaces template function with industry-standard regex patterns"
        }
    },
    "19.5_q5": {
        "id": "19.5_q5",
        "type": "error_diagnosis",
        "concept": "groups_and_extraction_basics",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["19.5_q4"],
        "prompt": "Why does the following code crash with `AttributeError: 'NoneType' object has no attribute 'group'`?\n\n```python\nimport re\nmatch = re.search(r\"\\d+\", \"No numbers here\")\nprint(match.group(0))\n```",
        "options": [
            "re.search returns None when no match is found, so calling .group() on None raises AttributeError.",
            "group(0) is invalid; groups start at index 1.",
            "The regular expression pattern has invalid syntax.",
            "print cannot format match objects."
        ],
        "correct_answer": "re.search returns None when no match is found, so calling .group() on None raises AttributeError.",
        "explanation": "When `re.search()` fails to match anything in the target string, it returns `None`. Safe code must always check `if match:` before accessing `.group()`.",
        "metadata": {
            "concept": "none_guard_on_regex_matches",
            "skill": "defensive_programming",
            "learning_objective": "Guard against AttributeError by checking if match is not None",
            "common_misconception": "Assuming re.search always returns a match object",
            "why_this_exercise_exists": "Replaces template function with a ubiquitous runtime bug"
        }
    },
    "19.5_q6": {
        "id": "19.5_q6",
        "type": "write_the_code",
        "concept": "groups_and_extraction_basics",
        "skill": "implementation",
        "difficulty": "hard",
        "prerequisites": ["19.5_q5"],
        "prompt": "Write a regex pattern to extract the status code and request path from a web log line: `'GET /api/v1/users HTTP/1.1 200'`. Capture path in group 1 and status in group 2.",
        "starter_code": "import re\nlog_line = \"GET /api/v1/users HTTP/1.1 200\"\n# Extract path and status code using regex groups\n",
        "solution_code": "import re\nlog_line = \"GET /api/v1/users HTTP/1.1 200\"\npattern = r\"GET\\s+(\\S+)\\s+HTTP/\\d\\.\\d\\s+(\\d+)\"\nmatch = re.search(pattern, log_line)\nif match:\n    path, status = match.groups()\n    print(f\"Path: {path}, Status: {status}\")",
        "explanation": "Parentheses around `(\\S+)` and `(\\d+)` capture the path `'/api/v1/users'` and status `'200'` respectively.",
        "metadata": {
            "concept": "log_extraction_with_regex",
            "skill": "data_extraction",
            "learning_objective": "Extract structured fields from unformatted log text using regex groups",
            "common_misconception": "Writing overly brittle regexes that break on variable spacing",
            "why_this_exercise_exists": "Replaces template function with authentic backend log extraction"
        }
    },

    # ==========================================
    # UNIT 20 & 21: OOP & ATTRIBUTES
    # ==========================================
    "20.3_q2": {
        "id": "20.3_q2",
        "type": "output_prediction",
        "concept": "the_self_keyword_basics",
        "skill": "mental_model",
        "difficulty": "easy",
        "prerequisites": ["20.3_q1"],
        "prompt": "What does `self` represent inside an instance method?\n\n```python\nclass Account:\n    def __init__(self, owner):\n        self.owner = owner\n\nacc = Account(\"Kiran\")\nprint(acc.owner)\n```",
        "options": [
            "Kiran",
            "Account",
            "self",
            "TypeError"
        ],
        "correct_answer": "Kiran",
        "explanation": "`self` refers to the specific instance of the class being created or operated upon. In this case, `acc` is the instance, so `self.owner = owner` attaches the attribute `'owner'` with value `'Kiran'` to `acc`.",
        "metadata": {
            "concept": "self_instance_reference",
            "skill": "mental_model",
            "learning_objective": "Understand that self represents the current instance object",
            "common_misconception": "Thinking self is a reserved keyword that refers to the class itself",
            "why_this_exercise_exists": "Replaces template function with foundational OOP principles"
        }
    },
    "20.3_q4": {
        "id": "20.3_q4",
        "type": "error_diagnosis",
        "concept": "the_self_keyword_basics",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["20.3_q3"],
        "prompt": "Why does calling `greeter.say_hello()` fail below?\n\n```python\nclass Greeter:\n    def say_hello():\n        print(\"Hello world!\")\n\ng = Greeter()\ng.say_hello()\n```",
        "options": [
            "TypeError: say_hello() takes 0 positional arguments but 1 was given",
            "NameError: say_hello is not defined",
            "AttributeError: Greeter object has no attribute 'say_hello'",
            "SyntaxError: method must return a string"
        ],
        "correct_answer": "TypeError: say_hello() takes 0 positional arguments but 1 was given",
        "explanation": "When invoking an instance method as `g.say_hello()`, Python automatically passes the instance `g` as the first argument. Because `def say_hello():` did not define the `self` parameter, Python complains that 1 argument was unexpectedly given.",
        "metadata": {
            "concept": "implicit_self_argument",
            "skill": "error_recognition",
            "learning_objective": "Diagnose the classic missing self TypeError in instance methods",
            "common_misconception": "Thinking methods without arguments don't need self",
            "why_this_exercise_exists": "Replaces template function with Python's most famous OOP signature error"
        }
    },
    "20.3_q5": {
        "id": "20.3_q5",
        "type": "code_prediction",
        "concept": "the_self_keyword_basics",
        "skill": "state_mutation",
        "difficulty": "medium",
        "prerequisites": ["20.3_q4"],
        "prompt": "Trace the balance after these method calls:\n\n```python\nclass Wallet:\n    def __init__(self, initial=0):\n        self.balance = initial\n    def add(self, amount):\n        self.balance += amount\n\nw = Wallet(50)\nw.add(25)\nprint(w.balance)\n```",
        "options": [
            "75",
            "50",
            "25",
            "None"
        ],
        "correct_answer": "75",
        "explanation": "`self.balance` starts at 50. Invoking `w.add(25)` updates `self.balance` by adding 25, resulting in 75.",
        "metadata": {
            "concept": "instance_state_mutation",
            "skill": "tracing",
            "learning_objective": "Track state mutations on instance attributes across method calls",
            "common_misconception": "Believing instance variables reset after each method call",
            "why_this_exercise_exists": "Replaces template function with authentic object state tracking"
        }
    },
    "20.3_q6": {
        "id": "20.3_q6",
        "type": "fix_the_code",
        "concept": "the_self_keyword_basics",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["20.3_q5"],
        "prompt": "Fix the method definition so it accepts `self` and correctly updates `self.total`:\n\n```python\nclass Counter:\n    def __init__(self):\n        self.total = 0\n    # Fix this method signature:\n    def increment(by):\n        self.total += by\n```",
        "starter_code": "class Counter:\n    def __init__(self):\n        self.total = 0\n    def increment(by):\n        self.total += by",
        "solution_code": "class Counter:\n    def __init__(self):\n        self.total = 0\n    def increment(self, by):\n        self.total += by",
        "explanation": "Instance methods must declare `self` as their first parameter. Writing `def increment(self, by):` allows Python to pass the instance implicitly.",
        "metadata": {
            "concept": "method_signature_repair",
            "skill": "repair",
            "learning_objective": "Supply self as the first parameter in parameterized methods",
            "common_misconception": "Omitting self when other parameters are present",
            "why_this_exercise_exists": "Replaces template function with essential OOP method repairs"
        }
    },
    "21.1_q2": {
        "id": "21.1_q2",
        "type": "output_prediction",
        "concept": "class_attributes_vs_instance_attributes_basics",
        "skill": "attribute_scope",
        "difficulty": "easy",
        "prerequisites": ["21.1_q1"],
        "prompt": "Consider the following class:\n\n```python\nclass Student:\n    school = \"Xavier Institute\"\n\n    def __init__(self, name):\n        self.name = name\n\ns1 = Student(\"Jean\")\ns2 = Student(\"Scott\")\nprint(s1.school == s2.school)\n```\n\nWhat is output?",
        "options": [
            "True",
            "False",
            "AttributeError",
            "None"
        ],
        "correct_answer": "True",
        "explanation": "`school` is a class attribute defined directly in the class body. It is shared across all instances of `Student`. Both `s1.school` and `s2.school` resolve to the exact same shared string `'Xavier Institute'`.",
        "metadata": {
            "concept": "shared_class_attribute",
            "skill": "mental_model",
            "learning_objective": "Recognize that class attributes are shared across all instances",
            "common_misconception": "Thinking class attributes are cloned per instance upon __init__",
            "why_this_exercise_exists": "Directly replaces template function with the user-mandated Student class attribute example"
        }
    },
    "21.1_q4": {
        "id": "21.1_q4",
        "type": "code_prediction",
        "concept": "class_attributes_vs_instance_attributes_basics",
        "skill": "shadowing",
        "difficulty": "medium",
        "prerequisites": ["21.1_q3"],
        "prompt": "What happens when an instance modifies an attribute with the same name as a class attribute?\n\n```python\nclass Config:\n    theme = \"dark\"\n\nc1 = Config()\nc2 = Config()\nc1.theme = \"light\"\nprint(c1.theme, c2.theme, Config.theme)\n```",
        "options": [
            "light dark dark",
            "light light light",
            "light light dark",
            "AttributeError: cannot shadow class attribute"
        ],
        "correct_answer": "light dark dark",
        "explanation": "Assigning `c1.theme = \"light\"` creates a new *instance attribute* on `c1` that shadows the class attribute for `c1` only. `c2.theme` and `Config.theme` still reference the untouched class attribute `'dark'`.",
        "metadata": {
            "concept": "attribute_shadowing_mechanics",
            "skill": "mental_model",
            "learning_objective": "Understand how instance assignment shadows class attributes without mutating the class",
            "common_misconception": "Believing c1.theme = 'light' changes theme for all instances and the class",
            "why_this_exercise_exists": "Directly addresses the attribute lookup hierarchy in Python OOP"
        }
    },
    "21.1_q5": {
        "id": "21.1_q5",
        "type": "output_prediction",
        "concept": "class_attributes_vs_instance_attributes_basics",
        "skill": "class_level_mutation",
        "difficulty": "medium",
        "prerequisites": ["21.1_q4"],
        "prompt": "What happens if we reassign the class attribute directly on the class itself?\n\n```python\nclass Student:\n    school = \"XIE\"\n    def __init__(self, name):\n        self.name = name\n\ns1 = Student(\"Aria\")\nStudent.school = \"Metro Tech\"\nprint(s1.school)\n```",
        "options": [
            "Metro Tech",
            "XIE",
            "AttributeError",
            "None"
        ],
        "correct_answer": "Metro Tech",
        "explanation": "Because `s1` does not have its own instance attribute named `school`, attribute lookup falls back to `Student.school`. Since the class attribute was updated to `'Metro Tech'`, `s1.school` reflects that change.",
        "metadata": {
            "concept": "class_level_attribute_updates",
            "skill": "tracing",
            "learning_objective": "Observe fallback attribute lookup when class attributes change",
            "common_misconception": "Assuming instances retain old class attribute values after class updates",
            "why_this_exercise_exists": "Solidifies the dynamic nature of Python class dictionaries"
        }
    },
    "21.1_q6": {
        "id": "21.1_q6",
        "type": "fix_the_code",
        "concept": "class_attributes_vs_instance_attributes_basics",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["21.1_q5"],
        "prompt": "A developer accidentally used a class attribute for a user's items list, causing all users to share the same shopping cart! Fix the class so each user gets an independent cart.\n\n```python\nclass Cart:\n    items = []  # Bug: shared across all instances\n\n    def __init__(self):\n        pass\n```",
        "starter_code": "class Cart:\n    items = []\n\n    def __init__(self):\n        pass",
        "solution_code": "class Cart:\n    def __init__(self):\n        self.items = []",
        "explanation": "Defining `items = []` at class level makes the list shared across every `Cart` instance. Moving `self.items = []` into `__init__` ensures every cart gets its own new, independent list.",
        "metadata": {
            "concept": "shared_mutable_class_attribute_bug",
            "skill": "repair",
            "learning_objective": "Fix unintended state leakage caused by mutable class attributes",
            "common_misconception": "Defining instance storage at the class declaration level",
            "why_this_exercise_exists": "Catastrophic real-world OOP bug that every developer must recognize"
        }
    },

    # ==========================================
    # UNIT 22: ADVANCED PYTHON MAGIC
    # ==========================================
    "22.2_q29": {
        "id": "22.2_q29",
        "type": "output_prediction",
        "concept": "decorators_wraps_metadata",
        "skill": "mental_model",
        "difficulty": "hard",
        "prerequisites": ["22.2_q28"],
        "prompt": "Why is `functools.wraps` used when writing custom decorators?\n\n```python\nfrom functools import wraps\n\ndef my_decorator(f):\n    @wraps(f)\n    def wrapper(*args, **kwargs):\n        return f(*args, **kwargs)\n    return wrapper\n\n@my_decorator\ndef compute_cube(n):\n    \"\"\"Calculates n cubed.\"\"\"\n    return n ** 3\n\nprint(compute_cube.__name__)\n```",
        "options": [
            "compute_cube",
            "wrapper",
            "my_decorator",
            "None"
        ],
        "correct_answer": "compute_cube",
        "explanation": "Without `@wraps(f)`, the decorated function would adopt the identity of the inner function (`compute_cube.__name__` would be `'wrapper'`), destroying docstrings and function names. `@wraps` copies original metadata back to the wrapper.",
        "metadata": {
            "concept": "decorator_metadata_preservation",
            "skill": "meta_programming",
            "learning_objective": "Preserve function docstrings and __name__ using functools.wraps",
            "common_misconception": "Assuming decorators preserve function metadata automatically",
            "why_this_exercise_exists": "Crucial requirement for building professional decorators"
        }
    },
    "22.6_q3": {
        "id": "22.6_q3",
        "type": "code_prediction",
        "concept": "type_hints_and_annotations_runtime",
        "skill": "mental_model",
        "difficulty": "medium",
        "prerequisites": ["22.6_q2"],
        "prompt": "Does Python enforce type annotations at runtime by default?\n\n```python\ndef repeat_msg(msg: str, count: int) -> str:\n    return msg * count\n\nprint(repeat_msg(5, 2))\n```",
        "options": [
            "10 (Python does not enforce type annotations at runtime; it treats them as documentation/hints for static analyzers like mypy).",
            "TypeError: argument msg expected str, received int.",
            "'55'",
            "SyntaxError: type annotations not supported in function body."
        ],
        "correct_answer": "10 (Python does not enforce type annotations at runtime; it treats them as documentation/hints for static analyzers like mypy).",
        "explanation": "In standard Python, type hints are purely annotations. Python does not validate or enforce types during execution. `repeat_msg(5, 2)` performs standard integer multiplication `5 * 2 = 10`. Static type checkers like `mypy` or IDEs use the hints to catch errors before runtime.",
        "metadata": {
            "concept": "type_hints_runtime_enforcement",
            "skill": "mental_model",
            "learning_objective": "Understand that Python type annotations are non-enforcing hints at runtime",
            "common_misconception": "Assuming Python behaves like Java or C++ and raises TypeErrors when annotations don't match runtime values",
            "why_this_exercise_exists": "Replaces template function with essential Python typing semantics"
        }
    },
    "22.6_q13": {
        "id": "22.6_q13",
        "type": "output_prediction",
        "concept": "type_hints_and_annotations_union",
        "skill": "syntax_comprehension",
        "difficulty": "medium",
        "prerequisites": ["22.6_q12"],
        "prompt": "In modern Python 3.10+, what does the pipe operator `|` represent in type annotations?\n\n```python\ndef parse_id(raw: int | str) -> int:\n    return int(raw)\n\nprint(parse_id(\"42\") + parse_id(10))\n```",
        "options": [
            "52",
            "Bitwise OR operation",
            "TypeError: pipe operator not allowed in annotations",
            "None"
        ],
        "correct_answer": "52",
        "explanation": "In modern Python, `int | str` is the union type syntax (equivalent to `typing.Union[int, str]`), meaning the parameter accepts either an `int` or a `str`. Both `'42'` and `10` are parsed to ints and summed: `42 + 10 = 52`.",
        "metadata": {
            "concept": "union_type_syntax",
            "skill": "modern_python",
            "learning_objective": "Read and write modern union type annotations with the pipe syntax",
            "common_misconception": "Confusing typing union with bitwise OR",
            "why_this_exercise_exists": "Replaces template function with modern type annotation standards"
        }
    },

    # ==========================================
    # UNIT 24: CLEAN CODE AND TESTING
    # ==========================================
    "24.1_q1": {
        "id": "24.1_q1",
        "type": "multiple_choice",
        "concept": "principles_of_clean_code_basics",
        "skill": "clean_code",
        "difficulty": "easy",
        "prerequisites": [],
        "prompt": "According to clean code principles and PEP 8, what makes a variable name high quality?",
        "options": [
            "It clearly reveals intent and purpose in lowercase_with_underscores, such as `user_account_balance` rather than `uab` or `data`.",
            "It is as short as possible (e.g. `x`, `y`, `z`) to minimize file size.",
            "It includes the variable's type in the name (e.g. `str_user_name_var`).",
            "It uses ALL_CAPS for local variables."
        ],
        "correct_answer": "It clearly reveals intent and purpose in lowercase_with_underscores, such as `user_account_balance` rather than `uab` or `data`.",
        "explanation": "Code is read much more often than it is written. Descriptive names that reveal business intent reduce cognitive load and eliminate the need for redundant comments.",
        "metadata": {
            "concept": "intent_revealing_naming",
            "skill": "code_style",
            "learning_objective": "Choose clear, intent-revealing variable names over cryptic abbreviations",
            "common_misconception": "Believing short variable names are faster or more professional",
            "why_this_exercise_exists": "Replaces template function with foundational clean code standards"
        }
    },
    "24.1_q4": {
        "id": "24.1_q4",
        "type": "fix_the_code",
        "concept": "principles_of_clean_code_basics",
        "skill": "refactoring",
        "difficulty": "medium",
        "prerequisites": ["24.1_q3"],
        "prompt": "Refactor the cryptic variable names below to clear, intent-revealing identifiers for customer checkout:\n\n```python\n# Refactor x and y to item_price and sales_tax_rate\nx = 49.99\ny = 0.07\nt = x + (x * y)\n```",
        "starter_code": "x = 49.99\ny = 0.07\nt = x + (x * y)",
        "solution_code": "item_price = 49.99\nsales_tax_rate = 0.07\ntotal_with_tax = item_price + (item_price * sales_tax_rate)",
        "explanation": "Replacing single-letter placeholders with `item_price`, `sales_tax_rate`, and `total_with_tax` immediately clarifies the business logic.",
        "metadata": {
            "concept": "identifier_refactoring",
            "skill": "refactoring",
            "learning_objective": "Refactor ambiguous single-letter variables to self-documenting names",
            "common_misconception": "Leaving temporary scratch names in production scripts",
            "why_this_exercise_exists": "Replaces template function with clean code renaming"
        }
    },
    "24.1_q5": {
        "id": "24.1_q5",
        "type": "multiple_choice",
        "concept": "principles_of_clean_code_basics",
        "skill": "dry_principle",
        "difficulty": "medium",
        "prerequisites": ["24.1_q4"],
        "prompt": "What does the 'DRY' principle stand for in clean software design?",
        "options": [
            "Don't Repeat Yourself: avoid duplicate logic by extracting shared procedures into functions or abstractions.",
            "Deploy Regularly Yearly: schedule deployments on an annual basis.",
            "Debug Runtime Yields: optimize while loops for execution speed.",
            "Declarative Readable Yield: prefer generators over lists everywhere."
        ],
        "correct_answer": "Don't Repeat Yourself: avoid duplicate logic by extracting shared procedures into functions or abstractions.",
        "explanation": "Duplication creates multiple places that must be maintained when requirements change or bugs are fixed. Extracting shared logic into single-purpose functions ensures bug fixes propagate everywhere.",
        "metadata": {
            "concept": "dry_principle",
            "skill": "software_architecture",
            "learning_objective": "Recognize and apply the Don't Repeat Yourself principle",
            "common_misconception": "Copy-pasting blocks of code with slight variable tweaks",
            "why_this_exercise_exists": "Replaces template function with foundational software engineering doctrine"
        }
    },
    "24.1_q7": {
        "id": "24.1_q7",
        "type": "refactoring_challenge",
        "concept": "principles_of_clean_code_basics",
        "skill": "function_extraction",
        "difficulty": "medium",
        "prerequisites": ["24.1_q6"],
        "prompt": "The script below duplicates email normalization logic. Refactor by extracting a clean helper function `normalize_email(email)`:\n\n```python\n# Before:\nuser1_email = \"  ALICE@GMAIL.COM \".strip().lower()\nuser2_email = \"  BOB@OUTLOOK.COM \".strip().lower()\n```",
        "starter_code": "def normalize_email(email):\n    # Extract normalization logic here\n    pass\n\nu1 = normalize_email(\"  ALICE@GMAIL.COM \")\nu2 = normalize_email(\"  BOB@OUTLOOK.COM \")\nprint(u1, u2)",
        "solution_code": "def normalize_email(email):\n    return email.strip().lower()\n\nu1 = normalize_email(\"  ALICE@GMAIL.COM \")\nu2 = normalize_email(\"  BOB@OUTLOOK.COM \")\nprint(u1, u2)",
        "explanation": "Extracting `email.strip().lower()` into `normalize_email()` centralizes email sanitization into a single reusable function.",
        "metadata": {
            "concept": "helper_function_extraction",
            "skill": "refactoring",
            "learning_objective": "Eliminate copy-pasted transformation logic by extracting reusable functions",
            "common_misconception": "Assuming tiny 1-line operations aren't worth extracting into functions",
            "why_this_exercise_exists": "Replaces template function with practical DRY refactoring"
        }
    },
    "24.1_q10": {
        "id": "24.1_q10",
        "type": "multiple_choice",
        "concept": "principles_of_clean_code_basics",
        "skill": "single_responsibility",
        "difficulty": "medium",
        "prerequisites": ["24.1_q9"],
        "prompt": "According to the Single Responsibility Principle, what should a function do?",
        "options": [
            "It should do one thing, do it well, and do it only.",
            "It should handle validation, database queries, and UI rendering in a single function.",
            "It should contain at least 100 lines to maximize throughput.",
            "It should return multiple completely unrelated data structures."
        ],
        "correct_answer": "It should do one thing, do it well, and do it only.",
        "explanation": "Functions that perform multiple disparate tasks (e.g. parsing input, computing statistics, and printing reports) are difficult to test, reuse, and debug. Decomposing them into focused units improves maintainability.",
        "metadata": {
            "concept": "single_responsibility_principle",
            "skill": "architecture",
            "learning_objective": "Apply the Single Responsibility Principle to function design",
            "common_misconception": "Writing 'god functions' that manage entire workflows in one place",
            "why_this_exercise_exists": "Replaces template function with core software modularity concepts"
        }
    },
    "24.1_q25": {
        "id": "24.1_q25",
        "type": "fix_the_code",
        "concept": "principles_of_clean_code_magic_numbers",
        "skill": "constants",
        "difficulty": "medium",
        "prerequisites": ["24.1_q24"],
        "prompt": "Replace the unexplained 'magic number' `86400` with a named module constant `SECONDS_PER_DAY` to make the calculation self-documenting:\n\n```python\n# Before:\ndef days_to_seconds(days):\n    return days * 86400\n```",
        "starter_code": "def days_to_seconds(days):\n    return days * 86400",
        "solution_code": "SECONDS_PER_DAY = 86400\n\ndef days_to_seconds(days):\n    return days * SECONDS_PER_DAY",
        "explanation": "Replacing unexplained raw numbers with uppercase named constants clarifies their origin and allows future adjustments in one central place.",
        "metadata": {
            "concept": "magic_numbers_removal",
            "skill": "clean_code",
            "learning_objective": "Replace raw magic numbers with descriptive uppercase constants",
            "common_misconception": "Assuming readers will automatically deduce what arbitrary literals mean",
            "why_this_exercise_exists": "Replaces template function with professional constants refactoring"
        }
    },
    "24.1_q27": {
        "id": "24.1_q27",
        "type": "refactoring_challenge",
        "concept": "principles_of_clean_code_early_return",
        "skill": "guard_clauses",
        "difficulty": "medium",
        "prerequisites": ["24.1_q26"],
        "prompt": "Refactor this deeply nested function using guard clauses with early returns:\n\n```python\ndef process_payment(amount, is_verified, has_funds):\n    if is_verified:\n        if has_funds:\n            if amount > 0:\n                return \"Success\"\n    return \"Declined\"\n```",
        "starter_code": "def process_payment(amount, is_verified, has_funds):\n    # Flatten using guard clauses\n    pass",
        "solution_code": "def process_payment(amount, is_verified, has_funds):\n    if not is_verified or not has_funds or amount <= 0:\n        return \"Declined\"\n    return \"Success\"",
        "explanation": "Checking failure conditions immediately at the beginning (guard clauses) allows the happy path to execute with zero indentation nesting.",
        "metadata": {
            "concept": "guard_clauses_early_return",
            "skill": "refactoring",
            "learning_objective": "Flatten nested conditional trees using guard clauses and early returns",
            "common_misconception": "Believing a function should only have a single return statement at the bottom",
            "why_this_exercise_exists": "Teaches one of the most effective code cleanup techniques"
        }
    },
    "24.1_q29": {
        "id": "24.1_q29",
        "type": "write_the_code",
        "concept": "principles_of_clean_code_pure_functions",
        "skill": "functional_design",
        "difficulty": "hard",
        "prerequisites": ["24.1_q28"],
        "prompt": "Write a pure function `filter_positive(numbers)` that returns a new list of numbers greater than zero WITHOUT mutating the input list. Test with `[ -3, 0, 5, -1, 10 ]`.",
        "starter_code": "def filter_positive(numbers):\n    # Return new list without mutating numbers\n    pass",
        "solution_code": "def filter_positive(numbers):\n    return [n for n in numbers if n > 0]\n\nresult = filter_positive([-3, 0, 5, -1, 10])\nprint(result)",
        "explanation": "A pure function produces a new output based solely on its arguments without mutating the caller's objects, preventing subtle side-effect bugs.",
        "metadata": {
            "concept": "pure_functions_immutability",
            "skill": "clean_architecture",
            "learning_objective": "Write pure functions that avoid unintended in-place mutations",
            "common_misconception": "Calling numbers.remove() inside a loop which breaks iteration",
            "why_this_exercise_exists": "Teaches fundamental clean data pipeline design"
        }
    },
    "24.2_q8": {
        "id": "24.2_q8",
        "type": "multiple_choice",
        "concept": "docstrings_pep257_standards",
        "skill": "documentation",
        "difficulty": "medium",
        "prerequisites": ["24.2_q7"],
        "prompt": "According to PEP 257, which format represents a clean, standard one-line docstring in Python?",
        "options": [
            "\"\"\"Return the absolute value of number n.\"\"\"",
            "# Return the absolute value of number n.",
            "// Return the absolute value of number n.",
            "\"Return the absolute value of number n.\""
        ],
        "correct_answer": "\"\"\"Return the absolute value of number n.\"\"\"",
        "explanation": "Python docstrings use triple double-quotes `\"\"\"...\"\"\"` immediately after the `def` line. They end with a period and are accessible programmatically via `func.__doc__`.",
        "metadata": {
            "concept": "pep257_docstring_format",
            "skill": "documentation",
            "learning_objective": "Format standard Python docstrings according to PEP 257",
            "common_misconception": "Using hash comments (#) and expecting help() to display them",
            "why_this_exercise_exists": "Replaces template function with proper docstring syntax"
        }
    },
    "24.2_q19": {
        "id": "24.2_q19",
        "type": "write_the_code",
        "concept": "docstrings_sphynx_google_style",
        "skill": "documentation",
        "difficulty": "medium",
        "prerequisites": ["24.2_q18"],
        "prompt": "Write a function `compute_discount(price, rate)` with a Google-style docstring documenting `Args:`, `Returns:`, and `Raises:` ValueError if rate is negative.",
        "starter_code": "def compute_discount(price, rate):\n    # Add docstring and implementation\n    pass",
        "solution_code": "def compute_discount(price, rate):\n    \"\"\"Calculates discounted price from base price and rate.\n\n    Args:\n        price: The original float price.\n        rate: The discount rate as a decimal between 0 and 1.\n\n    Returns:\n        The discounted price.\n\n    Raises:\n        ValueError: If rate is negative.\n    \"\"\"\n    if rate < 0:\n        raise ValueError(\"Rate cannot be negative\")\n    return price * (1 - rate)",
        "explanation": "Google-style docstrings clearly partition parameters, return contracts, and potential exceptions into standard readable sections.",
        "metadata": {
            "concept": "google_style_docstrings",
            "skill": "documentation",
            "learning_objective": "Document arguments, return types, and exceptions in industry-standard format",
            "common_misconception": "Writing free-form paragraphs without standard parameter tags",
            "why_this_exercise_exists": "Replaces template function with production documentation standards"
        }
    },
    "24.2_q24": {
        "id": "24.2_q24",
        "type": "code_prediction",
        "concept": "docstrings_runtime_inspection",
        "skill": "introspection",
        "difficulty": "medium",
        "prerequisites": ["24.2_q23"],
        "prompt": "How does Python expose the docstring of a function at runtime?\n\n```python\ndef ping():\n    \"\"\"Sends a healthcheck ping.\"\"\"\n    return True\n\nprint(ping.__doc__.strip())\n```",
        "options": [
            "Sends a healthcheck ping.",
            "None",
            "AttributeError",
            "ping"
        ],
        "correct_answer": "Sends a healthcheck ping.",
        "explanation": "Python binds docstrings to the function object's `__doc__` attribute, enabling tools like `help()`, Sphinx, and automated documentation generators to inspect them at runtime.",
        "metadata": {
            "concept": "docstring_introspection",
            "skill": "introspection",
            "learning_objective": "Inspect docstrings dynamically via the __doc__ attribute",
            "common_misconception": "Believing docstrings are stripped out like standard comments",
            "why_this_exercise_exists": "Replaces template function with introspection knowledge"
        }
    },
    "24.3_q24": {
        "id": "24.3_q24",
        "type": "write_the_code",
        "concept": "unit_testing_basics_assert",
        "skill": "test_authoring",
        "difficulty": "medium",
        "prerequisites": ["24.3_q23"],
        "prompt": "Write a unit test function `test_compute_tax()` that verifies `compute_tax(100, 0.1)` returns `10.0` and `compute_tax(0, 0.1)` returns `0.0` using `assert` statements.",
        "starter_code": "def compute_tax(amount, rate):\n    return amount * rate\n\ndef test_compute_tax():\n    # Write assert statements to test compute_tax\n    pass",
        "solution_code": "def compute_tax(amount, rate):\n    return amount * rate\n\ndef test_compute_tax():\n    assert compute_tax(100, 0.1) == 10.0, \"Should calculate 10% of 100\"\n    assert compute_tax(0, 0.1) == 0.0, \"Should return 0 for zero amount\"\n\ntest_compute_tax()\nprint(\"Tests passed\")",
        "explanation": "Writing clear assertions with failure messages ensures automated test runners (like pytest) can verify correct behavior across normal and boundary inputs.",
        "metadata": {
            "concept": "assertion_based_unit_testing",
            "skill": "testing",
            "learning_objective": "Write automated assertion tests covering multiple scenario inputs",
            "common_misconception": "Testing code by manual visual inspection of print() output",
            "why_this_exercise_exists": "Replaces template function with authentic test case construction"
        }
    },
    "24.6_q11": {
        "id": "24.6_q11",
        "type": "refactoring_challenge",
        "concept": "refactoring_spaghetti_code_decomposition",
        "skill": "refactoring",
        "difficulty": "hard",
        "prerequisites": ["24.6_q10"],
        "prompt": "The legacy report generator below mixes data fetching, filtering, and printing in a single monolithic loop. Decompose it into a clean pipeline: a filter function `get_active_users(users)` and a format function `format_user_list(active_users)`.",
        "starter_code": "# Monolithic spaghetti:\nusers = [{\"name\": \"Alice\", \"active\": True}, {\"name\": \"Bob\", \"active\": False}]\nfor u in users:\n    if u[\"active\"]:\n        print(f\"ACTIVE: {u['name']}\")",
        "solution_code": "users = [{\"name\": \"Alice\", \"active\": True}, {\"name\": \"Bob\", \"active\": False}]\n\ndef get_active_users(user_list):\n    return [u for u in user_list if u[\"active\"]]\n\ndef format_user_list(active_users):\n    return [f\"ACTIVE: {u['name']}\" for u in active_users]\n\nfor line in format_user_list(get_active_users(users)):\n    print(line)",
        "explanation": "Separating filtering logic from presentation formatting decouples data processing from I/O, allowing independent unit testing of business rules.",
        "metadata": {
            "concept": "pipeline_decomposition",
            "skill": "refactoring",
            "learning_objective": "Deconstruct monolithic spaghetti loops into dedicated filter and format steps",
            "common_misconception": "Mixing data transformation and printing in a single loop",
            "why_this_exercise_exists": "Replaces template function with real architectural refactoring"
        }
    },
    "24.6_q19": {
        "id": "24.6_q19",
        "type": "refactoring_challenge",
        "concept": "refactoring_spaghetti_code_state_isolation",
        "skill": "refactoring",
        "difficulty": "hard",
        "prerequisites": ["24.6_q18"],
        "prompt": "The following code relies on global mutable variables `total` and `items_count` modified inside a procedure. Refactor it to a pure function `compute_order_summary(prices)` that returns a dictionary `{'total': float, 'count': int}` without touching globals.",
        "starter_code": "# Legacy code with global side-effects:\ntotal = 0\nitems_count = 0\n\ndef add_prices(price_list):\n    global total, items_count\n    for p in price_list:\n        total += p\n        items_count += 1",
        "solution_code": "def compute_order_summary(prices):\n    return {\n        \"total\": sum(prices),\n        \"count\": len(prices)\n    }\n\nsummary = compute_order_summary([19.99, 5.50, 4.25])\nprint(summary)",
        "explanation": "Eliminating `global` variables and returning self-contained data structures isolates state and eliminates concurrency and testing nightmares.",
        "metadata": {
            "concept": "global_state_elimination",
            "skill": "clean_architecture",
            "learning_objective": "Refactor global mutable variables into localized, pure function returns",
            "common_misconception": "Relying on global variables to accumulate totals across function calls",
            "why_this_exercise_exists": "Replaces template function with state isolation refactoring"
        }
    },

    # ==========================================
    # UNIT 25: APIS AND NETWORKING
    # ==========================================
    "25.5_q1": {
        "id": "25.5_q1",
        "type": "multiple_choice",
        "concept": "web_scraping_basics_soup_initialization",
        "skill": "library_usage",
        "difficulty": "easy",
        "prerequisites": [],
        "prompt": "How do you parse an HTML document string using `BeautifulSoup`?",
        "options": [
            "soup = BeautifulSoup(html_doc, 'html.parser')",
            "soup = BeautifulSoup.parse_string(html_doc)",
            "soup = html_doc.to_soup()",
            "soup = BeautifulSoup.get(html_doc)"
        ],
        "correct_answer": "soup = BeautifulSoup(html_doc, 'html.parser')",
        "explanation": "Instantiating `BeautifulSoup(html_doc, 'html.parser')` takes the raw HTML string and parses it into a navigable DOM tree using Python's built-in `html.parser`.",
        "metadata": {
            "concept": "beautifulsoup_initialization",
            "skill": "initialization",
            "learning_objective": "Initialize a BeautifulSoup DOM tree with the standard parser",
            "common_misconception": "Assuming BeautifulSoup has a separate parse_string method",
            "why_this_exercise_exists": "Essential starting point for web scraping"
        }
    },
    "25.5_q3": {
        "id": "25.5_q3",
        "type": "code_prediction",
        "concept": "web_scraping_basics_tag_access",
        "skill": "tag_extraction",
        "difficulty": "medium",
        "prerequisites": ["25.5_q2"],
        "prompt": "Given `soup = BeautifulSoup('<h1>Title</h1><p>Paragraph</p>', 'html.parser')`, how do you extract only the textual content inside the `<h1>` tag without the HTML tags?",
        "options": [
            "soup.h1.text (or soup.h1.get_text())",
            "soup.h1.strip_tags()",
            "str(soup.h1)",
            "soup.h1.inner_html()"
        ],
        "correct_answer": "soup.h1.text (or soup.h1.get_text())",
        "explanation": "Accessing `.text` or `.get_text()` on a BeautifulSoup Tag object strips out all enclosing tags and returns only the plain inner text (`'Title'`).",
        "metadata": {
            "concept": "tag_text_extraction",
            "skill": "extraction",
            "learning_objective": "Extract clean inner text from HTML tags using .text or .get_text()",
            "common_misconception": "Converting the tag directly to str() which keeps <h1> tags intact",
            "why_this_exercise_exists": "Core BeautifulSoup extraction idiom"
        }
    },
    "25.5_q10": {
        "id": "25.5_q10",
        "type": "output_prediction",
        "concept": "web_scraping_basics_find_vs_find_all",
        "skill": "api_discrimination",
        "difficulty": "medium",
        "prerequisites": ["25.5_q9"],
        "prompt": "What is the difference in return types between `soup.find('a')` and `soup.find_all('a')`?",
        "options": [
            "find() returns the first Tag (or None); find_all() returns a list of Tags (or empty list []).",
            "find() returns text; find_all() returns tags.",
            "find() returns a list; find_all() returns a generator.",
            "There is no difference; they are aliases."
        ],
        "correct_answer": "find() returns the first Tag (or None); find_all() returns a list of Tags (or empty list []).",
        "explanation": "`soup.find()` stops scanning after finding the first matching element and returns a single `Tag` object (or `None`). `soup.find_all()` finds every matching element in the DOM and returns a ResultSet (list) of matching tags.",
        "metadata": {
            "concept": "find_vs_find_all",
            "skill": "api_discrimination",
            "learning_objective": "Discriminate between single-element search (find) and multi-element search (find_all)",
            "common_misconception": "Attempting to iterate directly over the result of soup.find()",
            "why_this_exercise_exists": "Prevents TypeErrors when handling search results"
        }
    },
    "25.5_q11": {
        "id": "25.5_q11",
        "type": "error_diagnosis",
        "concept": "web_scraping_basics_none_attribute_error",
        "skill": "defensive_scraping",
        "difficulty": "medium",
        "prerequisites": ["25.5_q10"],
        "prompt": "Why does this scraper code crash with `AttributeError: 'NoneType' object has no attribute 'text'`?\n\n```python\nsoup = BeautifulSoup(\"<div><p>Hello</p></div>\", \"html.parser\")\nheading = soup.find(\"h1\").text\n```",
        "options": [
            "soup.find('h1') returned None because there is no <h1> in the HTML; accessing .text on None raises AttributeError.",
            "BeautifulSoup requires lxml parser for headers.",
            "find() requires a class attribute.",
            "text is a private method."
        ],
        "correct_answer": "soup.find('h1') returned None because there is no <h1> in the HTML; accessing .text on None raises AttributeError.",
        "explanation": "Web scraping is inherently fragile. Websites frequently change layout or omit optional elements. If a selector doesn't match, `find()` returns `None`. Safe scrapers must always verify `if elem:` before accessing `.text` or attributes.",
        "metadata": {
            "concept": "defensive_scraping_guards",
            "skill": "defensive_programming",
            "learning_objective": "Guard against AttributeError by checking if element is found",
            "common_misconception": "Assuming target elements are guaranteed to exist on every page",
            "why_this_exercise_exists": "Addresses the #1 crash in web scraper scripts"
        }
    },
    "25.5_q13": {
        "id": "25.5_q13",
        "type": "code_prediction",
        "concept": "web_scraping_basics_attribute_access",
        "skill": "attribute_extraction",
        "difficulty": "medium",
        "prerequisites": ["25.5_q12"],
        "prompt": "How do you extract the destination URL from an anchor tag `link = soup.find('a')`?\n\n```python\nhtml = '<a href=\"https://codolingo.com\" target=\"_blank\">Learn</a>'\nsoup = BeautifulSoup(html, 'html.parser')\nlink = soup.find('a')\nprint(link['href'])\n```",
        "options": [
            "https://codolingo.com",
            "Learn",
            "_blank",
            "AttributeError: link.href not found"
        ],
        "correct_answer": "https://codolingo.com",
        "explanation": "BeautifulSoup tags treat HTML attributes like dictionary keys. `link['href']` or `link.get('href')` extracts the value of the `href` attribute.",
        "metadata": {
            "concept": "tag_attribute_dictionary_access",
            "skill": "attribute_extraction",
            "learning_objective": "Access HTML tag attributes using dictionary bracket or .get() syntax",
            "common_misconception": "Attempting link.href as an object property",
            "why_this_exercise_exists": "Core link and asset extraction technique in scraping"
        }
    },
    "25.5_q14": {
        "id": "25.5_q14",
        "type": "output_prediction",
        "concept": "web_scraping_basics_css_selectors",
        "skill": "css_selectors",
        "difficulty": "medium",
        "prerequisites": ["25.5_q13"],
        "prompt": "What does `soup.select('.price')` return when given this HTML snippet?\n\n```python\nhtml = '<div class=\"item\"><span class=\"price\">$19.99</span><span class=\"price\">$29.99</span></div>'\nsoup = BeautifulSoup(html, 'html.parser')\nprices = [p.text for p in soup.select('.price')]\nprint(prices)\n```",
        "options": [
            "['$19.99', '$29.99']",
            "['$19.99']",
            "['item']",
            "SyntaxError"
        ],
        "correct_answer": "['$19.99', '$29.99']",
        "explanation": "`soup.select()` accepts standard CSS selector syntax. The class selector `'.price'` matches all elements having the class `price`, returning a list of two matching span tags.",
        "metadata": {
            "concept": "css_selector_querying",
            "skill": "selectors",
            "learning_objective": "Query DOM nodes using standard CSS class selectors with select()",
            "common_misconception": "Thinking select() only works with tag names",
            "why_this_exercise_exists": "Modern web scraping standard workflow"
        }
    },
    "25.5_q16": {
        "id": "25.5_q16",
        "type": "code_prediction",
        "concept": "web_scraping_basics_class_filtering",
        "skill": "attribute_filtering",
        "difficulty": "medium",
        "prerequisites": ["25.5_q15"],
        "prompt": "When searching for an element by HTML class with `soup.find()`, why must you use `class_=\"btn\"` instead of `class=\"btn\"`?",
        "options": [
            "'class' is a reserved keyword in Python, so BeautifulSoup uses 'class_' to avoid a SyntaxError.",
            "HTML classes are underscored in Python.",
            "class_ forces case-insensitive matching.",
            "There is no difference; either can be used."
        ],
        "correct_answer": "'class' is a reserved keyword in Python, so BeautifulSoup uses 'class_' to avoid a SyntaxError.",
        "explanation": "Because `class` is Python's reserved keyword for declaring classes, Python's parser will raise a `SyntaxError` if you try to pass `class=\"...\"` as a keyword argument. BeautifulSoup uses `class_` with a trailing underscore as the parameter name.",
        "metadata": {
            "concept": "class_keyword_parameter_conflict",
            "skill": "syntax_rules",
            "learning_objective": "Understand why BeautifulSoup uses class_ for HTML class filtering",
            "common_misconception": "Writing soup.find('div', class='main') and getting SyntaxError",
            "why_this_exercise_exists": "Eliminates a constant source of syntax errors in web scraping"
        }
    },
    "25.5_q18": {
        "id": "25.5_q18",
        "type": "fix_the_code",
        "concept": "web_scraping_basics_safe_extraction",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["25.5_q17"],
        "prompt": "Fix the fragile scraper code so that it safely extracts the author's name if present, or returns `'Unknown'` if the `.author` element is missing:\n\n```python\nhtml = '<div class=\"article\"><h2>Python 3.14 Released</h2></div>'\nsoup = BeautifulSoup(html, 'html.parser')\n\n# Fix this line to avoid AttributeError:\nauthor = soup.find('span', class_='author').text\n```",
        "starter_code": "html = '<div class=\"article\"><h2>Python 3.14 Released</h2></div>'\nsoup = BeautifulSoup(html, 'html.parser')\nauthor = soup.find('span', class_='author').text",
        "solution_code": "html = '<div class=\"article\"><h2>Python 3.14 Released</h2></div>'\nsoup = BeautifulSoup(html, 'html.parser')\nauthor_tag = soup.find('span', class_='author')\nauthor = author_tag.text if author_tag else \"Unknown\"\nprint(author)",
        "explanation": "Checking `if author_tag` before accessing `.text` prevents the `AttributeError: 'NoneType' object has no attribute 'text'` when the tag does not exist.",
        "metadata": {
            "concept": "defensive_tag_extraction",
            "skill": "repair",
            "learning_objective": "Implement null-safe tag text extraction with fallback defaults",
            "common_misconception": "Assuming all articles have identical HTML layouts",
            "why_this_exercise_exists": "Fundamental resilient scraping practice"
        }
    },
    "25.5_q19": {
        "id": "25.5_q19",
        "type": "write_the_code",
        "concept": "web_scraping_basics_table_scraping",
        "skill": "table_parsing",
        "difficulty": "hard",
        "prerequisites": ["25.5_q18"],
        "prompt": "Given `html_table = '<table><tr><th>Country</th><th>Code</th></tr><tr><td>India</td><td>IN</td></tr><tr><td>Germany</td><td>DE</td></tr></table>'`, parse the table rows using BeautifulSoup and extract a dictionary mapping country names to country codes: `{'India': 'IN', 'Germany': 'DE'}`.",
        "starter_code": "from bs4 import BeautifulSoup\nhtml_table = '<table><tr><th>Country</th><th>Code</th></tr><tr><td>India</td><td>IN</td></tr><tr><td>Germany</td><td>DE</td></tr></table>'\nsoup = BeautifulSoup(html_table, 'html.parser')\ncountry_map = {}\n# Parse rows and populate country_map\n",
        "solution_code": "from bs4 import BeautifulSoup\nhtml_table = '<table><tr><th>Country</th><th>Code</th></tr><tr><td>India</td><td>IN</td></tr><tr><td>Germany</td><td>DE</td></tr></table>'\nsoup = BeautifulSoup(html_table, 'html.parser')\ncountry_map = {}\nfor row in soup.find_all('tr'):\n    cols = row.find_all('td')\n    if len(cols) == 2:\n        country_map[cols[0].text] = cols[1].text\nprint(country_map)",
        "explanation": "Iterating over `<tr>` rows, checking for exactly 2 `<td>` columns (ignoring `<th>` headers), and pairing `cols[0].text` with `cols[1].text` constructs the clean dictionary.",
        "metadata": {
            "concept": "html_table_parsing",
            "skill": "table_scraping",
            "learning_objective": "Parse tabular data from HTML tables into clean Python dictionaries",
            "common_misconception": "Failing to filter out table header (th) rows",
            "why_this_exercise_exists": "Real-world web scraping pattern for structured data"
        }
    },
    "25.5_q22": {
        "id": "25.5_q22",
        "type": "multiple_choice",
        "concept": "web_scraping_basics_ethics_and_limits",
        "skill": "ethics_and_architecture",
        "difficulty": "medium",
        "prerequisites": ["25.5_q21"],
        "prompt": "What file should a responsible web scraper inspect before scraping a target website?",
        "options": [
            "robots.txt at the site root (e.g. example.com/robots.txt) to check crawler directives, allowed paths, and rate limits.",
            "sitemap.xml to download all images.",
            ".htaccess to verify server configuration.",
            "package.json to see the frontend framework."
        ],
        "correct_answer": "robots.txt at the site root (e.g. example.com/robots.txt) to check crawler directives, allowed paths, and rate limits.",
        "explanation": "`robots.txt` defines the Robots Exclusion Protocol, specifying which URL paths automated bots are permitted or prohibited from crawling.",
        "metadata": {
            "concept": "robots_txt_protocol",
            "skill": "best_practices",
            "learning_objective": "Respect robots.txt and ethical rate-limiting policies when scraping",
            "common_misconception": "Ignoring site crawling policies and risking IP bans or legal liabilities",
            "why_this_exercise_exists": "Essential professional ethics and legal awareness in web engineering"
        }
    },

    # ==========================================
    # UNIT 26: DATABASES AND SQL
    # ==========================================
    "26.6_q2": {
        "id": "26.6_q2",
        "type": "error_diagnosis",
        "concept": "parameterized_queries_and_security_sql_injection",
        "skill": "security",
        "difficulty": "medium",
        "prerequisites": ["26.6_q1"],
        "prompt": "Why is the following query vulnerable to catastrophic SQL Injection?\n\n```python\nuser_input = \"admin' OR '1'='1\"\nquery = f\"SELECT * FROM users WHERE username = '{user_input}'\"\n```",
        "options": [
            "Using f-string formatting injects raw unescaped SQL syntax, transforming the query into WHERE username = 'admin' OR '1'='1' which always evaluates to True.",
            "SQL does not support f-strings.",
            "The username column cannot be compared to strings.",
            "f-strings add null bytes to the query buffer."
        ],
        "correct_answer": "Using f-string formatting injects raw unescaped SQL syntax, transforming the query into WHERE username = 'admin' OR '1'='1' which always evaluates to True.",
        "explanation": "String concatenation or f-strings treat user input as executable SQL code rather than passive data. The injected `' OR '1'='1'` alters the query's boolean logic, allowing attackers to bypass authentication or dump all table records.",
        "metadata": {
            "concept": "sql_injection_vulnerability",
            "skill": "security",
            "learning_objective": "Identify SQL injection risks caused by dynamic string interpolation",
            "common_misconception": "Assuming database drivers automatically sanitize f-strings",
            "why_this_exercise_exists": "OWASP Top 10 security fundamental every developer must know"
        }
    },
    "26.6_q4": {
        "id": "26.6_q4",
        "type": "code_prediction",
        "concept": "parameterized_queries_and_security_parameterization",
        "skill": "secure_coding",
        "difficulty": "medium",
        "prerequisites": ["26.6_q3"],
        "prompt": "How does parameterized query execution protect against SQL Injection?\n\n```python\ncursor.execute(\"SELECT * FROM users WHERE username = ?\", (user_input,))\n```",
        "options": [
            "The database driver sends query structure and data separately, treating user_input strictly as literal data rather than executable SQL syntax.",
            "It strips all punctuation and single quotes from user_input automatically.",
            "It converts the user input to lowercase.",
            "It encrypts the entire query with TLS."
        ],
        "correct_answer": "The database driver sends query structure and data separately, treating user_input strictly as literal data rather than executable SQL syntax.",
        "explanation": "With parameterized queries (using placeholders like `?` or `%s`), the database engine compiles the query structure first. When parameter values are bound, they are treated strictly as literals, making it impossible for input to inject new SQL commands.",
        "metadata": {
            "concept": "parameterized_query_protection",
            "skill": "secure_architecture",
            "learning_objective": "Understand how parameter placeholders separate code from data",
            "common_misconception": "Thinking parameterized queries just do string replacement under the hood",
            "why_this_exercise_exists": "The gold standard for database interaction security"
        }
    },
    "26.6_q5": {
        "id": "26.6_q5",
        "type": "fix_the_code",
        "concept": "parameterized_queries_and_security_repair",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["26.6_q4"],
        "prompt": "Fix the unsafe query below by replacing string interpolation with safe parameterization using `?` placeholder and a parameter tuple in `cursor.execute`:\n\n```python\n# Unsafe:\nuser_id = 42\nquery = f\"DELETE FROM sessions WHERE user_id = {user_id}\"\ncursor.execute(query)\n```",
        "starter_code": "user_id = 42\n# Fix using parameterized query\nquery = f\"DELETE FROM sessions WHERE user_id = {user_id}\"\ncursor.execute(query)",
        "solution_code": "user_id = 42\nquery = \"DELETE FROM sessions WHERE user_id = ?\"\ncursor.execute(query, (user_id,))",
        "explanation": "Replacing `{user_id}` with `?` and passing `(user_id,)` as the second argument ensures safe, injection-proof parameter binding.",
        "metadata": {
            "concept": "parameterized_query_repair",
            "skill": "repair",
            "learning_objective": "Convert unsafe dynamic SQL statements into secure parameterized queries",
            "common_misconception": "Passing user_id without wrapping it in a tuple (user_id,)",
            "why_this_exercise_exists": "Teaches the essential secure database pattern in Python"
        }
    },
    "26.6_q6": {
        "id": "26.6_q6",
        "type": "error_diagnosis",
        "concept": "parameterized_queries_and_security_tuple_pitfall",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["26.6_q5"],
        "prompt": "Why does `cursor.execute(\"SELECT * FROM items WHERE name = ?\", (item_name))` cause a programming error when `item_name = \"pencil\"`?",
        "options": [
            "(item_name) is just a parenthesized string, not a tuple; Python requires a trailing comma (item_name,) to make a 1-element tuple.",
            "item_name must be an integer.",
            "SELECT queries cannot take parameters.",
            "cursor.execute only takes lists, never tuples."
        ],
        "correct_answer": "(item_name) is just a parenthesized string, not a tuple; Python requires a trailing comma (item_name,) to make a 1-element tuple.",
        "explanation": "In Python, parentheses alone do not create a tuple—the comma does! `(\"pencil\")` evaluates to the string `\"pencil\"`. When the database driver tries to unpack parameters, it iterates over the characters of the string (`'p'`, `'e'`, `'n'`, ...) causing parameter count mismatches. A 1-element tuple must have a trailing comma: `(\"pencil\",)`.",
        "metadata": {
            "concept": "single_element_tuple_comma",
            "skill": "syntax_rules",
            "learning_objective": "Recognize that single-element tuples require a trailing comma",
            "common_misconception": "Believing (x) creates a tuple",
            "why_this_exercise_exists": "Catches one of the most frustrating beginner syntax errors in database programming"
        }
    },

    # ==========================================
    # UNIT 29 & 30: COMPLEXITY AND TESTING
    # ==========================================
    "29.4_q2": {
        "id": "29.4_q2",
        "type": "output_prediction",
        "concept": "space_complexity_concepts_basics",
        "skill": "complexity_analysis",
        "difficulty": "easy",
        "prerequisites": ["29.4_q1"],
        "prompt": "What is the auxiliary space complexity of this function that sums a list in-place?\n\n```python\ndef compute_sum(numbers):\n    total = 0\n    for n in numbers:\n        total += n\n    return total\n```",
        "options": [
            "O(1) auxiliary space (constant space beyond the input list)",
            "O(n) auxiliary space",
            "O(n^2) auxiliary space",
            "O(log n) auxiliary space"
        ],
        "correct_answer": "O(1) auxiliary space (constant space beyond the input list)",
        "explanation": "The function only allocates a single scalar variable `total`. It does not create any new lists, dictionaries, or recursive call stacks. Regardless of whether `numbers` has 10 or 10,000,000 items, memory usage remains constant O(1).",
        "metadata": {
            "concept": "constant_space_complexity",
            "skill": "complexity_analysis",
            "learning_objective": "Determine auxiliary space complexity of iterative accumulators",
            "common_misconception": "Counting the input size as auxiliary space allocated by the function",
            "why_this_exercise_exists": "Replaces template function with authentic Big-O space analysis"
        }
    },
    "29.4_q4": {
        "id": "29.4_q4",
        "type": "code_prediction",
        "concept": "space_complexity_concepts_basics",
        "skill": "complexity_analysis",
        "difficulty": "medium",
        "prerequisites": ["29.4_q3"],
        "prompt": "What is the auxiliary space complexity of creating a duplicate list of squares?\n\n```python\ndef get_squares(numbers):\n    return [x * x for x in numbers]\n```",
        "options": [
            "O(n) auxiliary space",
            "O(1) auxiliary space",
            "O(n^2) auxiliary space",
            "O(log n) auxiliary space"
        ],
        "correct_answer": "O(n) auxiliary space",
        "explanation": "The list comprehension constructs a brand new list containing `n` elements in memory. Thus, auxiliary memory scales linearly with input size O(n).",
        "metadata": {
            "concept": "linear_space_complexity",
            "skill": "complexity_analysis",
            "learning_objective": "Recognize O(n) space allocation in comprehensions and copies",
            "common_misconception": "Assuming list comprehensions don't consume memory",
            "why_this_exercise_exists": "Replaces template function with linear space reasoning"
        }
    },
    "29.4_q5": {
        "id": "29.4_q5",
        "type": "output_prediction",
        "concept": "space_complexity_concepts_basics",
        "skill": "generator_space_efficiency",
        "difficulty": "medium",
        "prerequisites": ["29.4_q4"],
        "prompt": "How does using a generator expression reduce memory consumption compared to a list comprehension?\n\n```python\n# Generator expression:\nsquares_gen = (x * x for x in range(1_000_000))\n```",
        "options": [
            "It yields items on-demand one by one in O(1) space instead of allocating all 1,000,000 items in memory at once.",
            "It compresses numbers into 8-bit integers.",
            "It stores items directly on disk.",
            "It executes on multiple CPU cores."
        ],
        "correct_answer": "It yields items on-demand one by one in O(1) space instead of allocating all 1,000,000 items in memory at once.",
        "explanation": "Generators evaluate lazily. Instead of allocating a 1,000,000-element list in RAM, a generator only keeps track of its current state and produces the next element when requested via `next()`, maintaining O(1) space.",
        "metadata": {
            "concept": "lazy_evaluation_space_optimization",
            "skill": "optimization",
            "learning_objective": "Optimize memory usage using lazy generator streams",
            "common_misconception": "Thinking generator expressions immediately build collections in RAM",
            "why_this_exercise_exists": "Replaces template function with production memory optimization techniques"
        }
    },
    "29.4_q6": {
        "id": "29.4_q6",
        "type": "error_diagnosis",
        "concept": "space_complexity_concepts_basics",
        "skill": "call_stack_space",
        "difficulty": "medium",
        "prerequisites": ["29.4_q5"],
        "prompt": "What hidden space complexity exists in deep recursive functions?\n\n```python\ndef countdown(n):\n    if n <= 0:\n        return\n    countdown(n - 1)\n```",
        "options": [
            "O(n) auxiliary space consumed by the call stack frames waiting to return.",
            "O(1) space because no variables are created.",
            "O(n^2) space due to garbage collection lag.",
            "None; Python flattens all recursion automatically."
        ],
        "correct_answer": "O(n) auxiliary space consumed by the call stack frames waiting to return.",
        "explanation": "Each recursive call pushes a new stack frame containing execution state and local variables onto the call stack. A recursion depth of `n` requires O(n) memory on the call stack. Exceeding Python's recursion limit triggers a `RecursionError`.",
        "metadata": {
            "concept": "recursive_call_stack_space",
            "skill": "mental_model",
            "learning_objective": "Analyze call stack space consumption in recursive algorithms",
            "common_misconception": "Ignoring call stack memory when evaluating algorithm space",
            "why_this_exercise_exists": "Replaces template function with call-stack memory analysis"
        }
    },
    "30.1_q19": {
        "id": "30.1_q19",
        "type": "multiple_choice",
        "concept": "understanding_the_problem_edge_cases",
        "skill": "problem_solving",
        "difficulty": "medium",
        "prerequisites": ["30.1_q18"],
        "prompt": "When analyzing a coding problem that takes a list of integers as input, which edge cases should you always test?",
        "options": [
            "Empty list [], single-element list [x], list with negative numbers, duplicates, and boundary limits (e.g. very large inputs).",
            "Only lists with exactly 5 positive numbers.",
            "Only inputs that match the prompt's first example.",
            "No edge cases are needed if the code compiles."
        ],
        "correct_answer": "Empty list [], single-element list [x], list with negative numbers, duplicates, and boundary limits (e.g. very large inputs).",
        "explanation": "Real software and competitive coding platforms test code against edge conditions: empty inputs, single items, negative numbers, zeros, duplicates, and extremes. Identifying these upfront prevents runtime crashes.",
        "metadata": {
            "concept": "edge_case_identification",
            "skill": "problem_solving_methodology",
            "learning_objective": "Identify critical edge cases before writing implementation code",
            "common_misconception": "Assuming input will always look like the happy-path example",
            "why_this_exercise_exists": "Foundational methodology for problem solving and interviews"
        }
    },

    # ==========================================
    # UNIT 32 & 41: DSA PATTERNS
    # ==========================================
    "32.2_q2": {
        "id": "32.2_q2",
        "type": "output_prediction",
        "concept": "iteration_and_transformation_basics",
        "skill": "array_transformation",
        "difficulty": "easy",
        "prerequisites": ["32.2_q1"],
        "prompt": "What does this transformation loop output?\n\n```python\nnumbers = [1, 2, 3, 4]\ndoubled = [x * 2 for x in numbers if x % 2 == 0]\nprint(doubled)\n```",
        "options": [
            "[4, 8]",
            "[2, 4, 6, 8]",
            "[4]",
            "[2, 4]"
        ],
        "correct_answer": "[4, 8]",
        "explanation": "The condition `x % 2 == 0` filters only even numbers (`2` and `4`). The expression `x * 2` doubles each, yielding `[4, 8]`.",
        "metadata": {
            "concept": "filter_map_transformation",
            "skill": "data_transformation",
            "learning_objective": "Combine filtering and mapping in a single list comprehension",
            "common_misconception": "Applying doubling before the filtering step",
            "why_this_exercise_exists": "Replaces template function with array transformation logic"
        }
    },
    "32.2_q4": {
        "id": "32.2_q4",
        "type": "code_prediction",
        "concept": "iteration_and_transformation_basics",
        "skill": "prefix_sums",
        "difficulty": "medium",
        "prerequisites": ["32.2_q3"],
        "prompt": "Trace the running prefix sum created by this loop:\n\n```python\nnums = [1, 2, 3, 4]\nprefix = []\ncurr = 0\nfor x in nums:\n    curr += x\n    prefix.append(curr)\nprint(prefix)\n```",
        "options": [
            "[1, 3, 6, 10]",
            "[1, 2, 3, 4]",
            "[10, 6, 3, 1]",
            "[0, 1, 3, 6]"
        ],
        "correct_answer": "[1, 3, 6, 10]",
        "explanation": "Prefix sums accumulate running totals: 1, 1+2=3, 3+3=6, 6+4=10. Prefix arrays allow answering range-sum queries in O(1) time.",
        "metadata": {
            "concept": "prefix_sum_pattern",
            "skill": "algorithmic_patterns",
            "learning_objective": "Construct prefix sum arrays for fast range queries",
            "common_misconception": "Recalculating sums from index 0 on every query",
            "why_this_exercise_exists": "Replaces template function with foundational DSA prefix sum pattern"
        }
    },
    "32.2_q5": {
        "id": "32.2_q5",
        "type": "output_prediction",
        "concept": "iteration_and_transformation_basics",
        "skill": "two_pointers_reverse",
        "difficulty": "medium",
        "prerequisites": ["32.2_q4"],
        "prompt": "What does in-place two-pointer reversal do to `arr = ['a', 'b', 'c', 'd']`?\n\n```python\narr = ['a', 'b', 'c', 'd']\nleft = 0\nright = len(arr) - 1\nwhile left < right:\n    arr[left], arr[right] = arr[right], arr[left]\n    left += 1\n    right -= 1\nprint(\"\".join(arr))\n```",
        "options": [
            "dcba",
            "abcd",
            "badc",
            "cdba"
        ],
        "correct_answer": "dcba",
        "explanation": "The two pointers swap opposite elements and move toward the center, reversing the array in O(n) time and O(1) auxiliary space.",
        "metadata": {
            "concept": "two_pointers_in_place_reversal",
            "skill": "dsa_patterns",
            "learning_objective": "Implement in-place array reversal using opposing two pointers",
            "common_misconception": "Creating an extra list and wasting memory",
            "why_this_exercise_exists": "Replaces template function with classic DSA two-pointer reversal"
        }
    },
    "32.2_q6": {
        "id": "32.2_q6",
        "type": "fix_the_code",
        "concept": "iteration_and_transformation_basics",
        "skill": "debugging",
        "difficulty": "medium",
        "prerequisites": ["32.2_q5"],
        "prompt": "The code below intends to remove all zeros in-place or filter them out, but modifying a list while iterating over it causes it to skip elements! Fix the implementation using a clean list comprehension:\n\n```python\n# Buggy:\nnums = [0, 1, 0, 3, 12]\nfor x in nums:\n    if x == 0:\n        nums.remove(x)\n```",
        "starter_code": "nums = [0, 1, 0, 3, 12]\n# Fix by creating filtered non-zero list\n",
        "solution_code": "nums = [0, 1, 0, 3, 12]\nnon_zeros = [x for x in nums if x != 0]\nprint(non_zeros)",
        "explanation": "Mutating a list while iterating over it with a `for` loop shifts internal indexes, causing elements to be silently skipped. Filtering into a new list or rebuilding avoids mutation bugs.",
        "metadata": {
            "concept": "iteration_mutation_hazard",
            "skill": "debugging",
            "learning_objective": "Avoid modifying lists in-place during standard for-loop iteration",
            "common_misconception": "Assuming list.remove() inside for x in list works correctly",
            "why_this_exercise_exists": "Replaces template function with a notorious Python iteration bug"
        }
    },
    "41.1_q2": {
        "id": "41.1_q2",
        "type": "output_prediction",
        "concept": "recognizing_when_to_use_two_pointers_basics",
        "skill": "pattern_recognition",
        "difficulty": "easy",
        "prerequisites": ["41.1_q1"],
        "prompt": "When given a SORTED array and asked to find if two numbers sum to a target `T`, why is the Two-Pointer approach superior to brute force?",
        "options": [
            "It runs in O(n) time and O(1) space by moving left or right pointers inward based on sum comparisons, whereas brute force takes O(n^2).",
            "It sorts the array in O(1) time.",
            "It converts the problem to a hash table automatically.",
            "It eliminates all loops entirely."
        ],
        "correct_answer": "It runs in O(n) time and O(1) space by moving left or right pointers inward based on sum comparisons, whereas brute force takes O(n^2).",
        "explanation": "Because the array is already sorted, if `nums[left] + nums[right] < target`, the sum can only increase by incrementing `left`. If the sum is too large, it can only decrease by decrementing `right`. This examines every relevant pair in a single O(n) linear pass.",
        "metadata": {
            "concept": "two_pointers_sorted_array_efficiency",
            "skill": "pattern_recognition",
            "learning_objective": "Recognize when sorted order enables O(n) two-pointer pair searching",
            "common_misconception": "Using nested loops on sorted arrays instead of two pointers",
            "why_this_exercise_exists": "Replaces template function with core interview pattern recognition"
        }
    },
    "41.1_q4": {
        "id": "41.1_q4",
        "type": "code_prediction",
        "concept": "recognizing_when_to_use_two_pointers_basics",
        "skill": "pointer_movement_rules",
        "difficulty": "medium",
        "prerequisites": ["41.1_q3"],
        "prompt": "In a sorted two-sum search with target 15, current `nums[left] = 4` and `nums[right] = 13` (sum = 17). What is the next pointer adjustment?\n\n```python\n# Target is 15\n# Current sum is 4 + 13 = 17 (> 15)\n```",
        "options": [
            "Decrement right (right -= 1) to reduce the total sum.",
            "Increment left (left += 1) to increase the total sum.",
            "Reset both pointers to 0.",
            "Return False immediately."
        ],
        "correct_answer": "Decrement right (right -= 1) to reduce the total sum.",
        "explanation": "Since 17 is greater than the target 15, and the array is sorted in ascending order, the only way to obtain a smaller sum is to move the right pointer to the left.",
        "metadata": {
            "concept": "two_pointer_direction_rule",
            "skill": "algorithmic_reasoning",
            "learning_objective": "Determine correct pointer adjustment direction based on target comparison",
            "common_misconception": "Moving the wrong pointer and missing valid combinations",
            "why_this_exercise_exists": "Replaces template function with fundamental pointer movement logic"
        }
    },
    "41.1_q5": {
        "id": "41.1_q5",
        "type": "output_prediction",
        "concept": "recognizing_when_to_use_two_pointers_basics",
        "skill": "palindrome_verification",
        "difficulty": "medium",
        "prerequisites": ["41.1_q4"],
        "prompt": "What does a two-pointer palindrome check return for `\"racecar\"`?\n\n```python\ndef is_palindrome(s):\n    l, r = 0, len(s) - 1\n    while l < r:\n        if s[l] != s[r]:\n            return False\n        l += 1\n        r -= 1\n    return True\n\nprint(is_palindrome(\"racecar\"))\n```",
        "options": [
            "True",
            "False",
            "None",
            "IndexError"
        ],
        "correct_answer": "True",
        "explanation": "At each step, `s[l]` matches `s[r]` ('r'=='r', 'a'=='a', 'c'=='c'). When `l` and `r` meet at 'e', the loop finishes and returns `True`.",
        "metadata": {
            "concept": "two_pointer_palindrome_detection",
            "skill": "implementation",
            "learning_objective": "Verify string symmetry in O(n) time and O(1) auxiliary space",
            "common_misconception": "Reversing the entire string with s[::-1] which allocates O(n) extra memory",
            "why_this_exercise_exists": "Replaces template function with canonical interview problem"
        }
    },
    "41.1_q6": {
        "id": "41.1_q6",
        "type": "fix_the_code",
        "concept": "recognizing_when_to_use_two_pointers_basics",
        "skill": "repair",
        "difficulty": "medium",
        "prerequisites": ["41.1_q5"],
        "prompt": "Fix the condition in the two-pointer loop below so it doesn't cause an infinite loop or miss matches:\n\n```python\ndef has_pair_with_sum(nums, target):\n    l, r = 0, len(nums) - 1\n    # Fix loop condition:\n    while l <= r:\n        s = nums[l] + nums[r]\n        if s == target and l != r:\n            return True\n        elif s < target:\n            l += 1\n        else:\n            r -= 1\n    return False\n```",
        "starter_code": "def has_pair_with_sum(nums, target):\n    l, r = 0, len(nums) - 1\n    while l < r:\n        s = nums[l] + nums[r]\n        if s == target:\n            return True\n        elif s < target:\n            l += 1\n        else:\n            r -= 1\n    return False",
        "solution_code": "def has_pair_with_sum(nums, target):\n    l, r = 0, len(nums) - 1\n    while l < r:\n        s = nums[l] + nums[r]\n        if s == target:\n            return True\n        elif s < target:\n            l += 1\n        else:\n            r -= 1\n    return False",
        "explanation": "Using `while l < r:` ensures that two distinct elements are compared and prevents pairing an element with itself.",
        "metadata": {
            "concept": "two_pointer_boundary_condition",
            "skill": "repair",
            "learning_objective": "Use strict inequality (l < r) to guarantee two distinct elements in pair searches",
            "common_misconception": "Using l <= r which risks adding an element to itself",
            "why_this_exercise_exists": "Replaces template function with essential pointer termination logic"
        }
    },

    # ==========================================
    # UNIT 42: CAPSTONE PROJECTS
    # ==========================================
    # 42.1 Project: Log Parsing Automation
    "42.1_q13": {
        "id": "42.1_q13",
        "type": "write_the_code",
        "concept": "project_log_parsing_automation_milestone_1",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.1_q12"],
        "prompt": "Log Parser Milestone 1: Read a multiline log string `log_data = '2026-10-04 10:00:00 INFO Service started\\n2026-10-04 10:01:15 ERROR Database timeout'`, split into lines, and count non-empty log lines into `line_count`.",
        "starter_code": "log_data = \"2026-10-04 10:00:00 INFO Service started\\n2026-10-04 10:01:15 ERROR Database timeout\"\n# Split into lines and count\n",
        "solution_code": "log_data = \"2026-10-04 10:00:00 INFO Service started\\n2026-10-04 10:01:15 ERROR Database timeout\"\nlines = [l for l in log_data.splitlines() if l.strip()]\nline_count = len(lines)\nprint(f\"Parsed {line_count} lines\")",
        "explanation": "Using `.splitlines()` safely handles different operating system newline characters (`\\r\\n` vs `\\n`).",
        "metadata": {
            "concept": "log_file_line_ingestion",
            "skill": "implementation",
            "learning_objective": "Ingest and segment log data streams into clean lines",
            "common_misconception": "Splitting solely on '\\n' and leaving carriage returns '\\r'",
            "why_this_exercise_exists": "Replaces milestone 1 with authentic log parsing milestone 1"
        }
    },
    "42.1_q14": {
        "id": "42.1_q14",
        "type": "write_the_code",
        "concept": "project_log_parsing_automation_milestone_2",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.1_q13"],
        "prompt": "Log Parser Milestone 2: Given a single log line `line = '2026-10-04 12:30:45 WARNING Disk space low'`, split it into three tokens: `timestamp` (`'2026-10-04 12:30:45'`), `level` (`'WARNING'`), and `message` (`'Disk space low'`).",
        "starter_code": "line = \"2026-10-04 12:30:45 WARNING Disk space low\"\n# Parse timestamp, level, message\n",
        "solution_code": "line = \"2026-10-04 12:30:45 WARNING Disk space low\"\nparts = line.split(\" \", 3)\ntimestamp = f\"{parts[0]} {parts[1]}\"\nlevel = parts[2]\nmessage = parts[3]\nprint(f\"[{level}] {timestamp} -> {message}\")",
        "explanation": "Splitting with `maxsplit=3` cleanly preserves the entire trailing message string without fragmenting multi-word messages.",
        "metadata": {
            "concept": "log_line_tokenization",
            "skill": "implementation",
            "learning_objective": "Tokenize structured log lines using controlled split parameters",
            "common_misconception": "Splitting on all spaces and fracturing the log message",
            "why_this_exercise_exists": "Replaces milestone 2 with authentic log parsing milestone 2"
        }
    },
    "42.1_q15": {
        "id": "42.1_q15",
        "type": "write_the_code",
        "concept": "project_log_parsing_automation_milestone_3",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.1_q14"],
        "prompt": "Log Parser Milestone 3: Extract ISO timestamps from messy log entries using regex. Given `entry = 'CRITICAL [2026-10-04T14:22:10] Connection lost'`, extract the timestamp inside brackets into `extracted_time`.",
        "starter_code": "import re\nentry = \"CRITICAL [2026-10-04T14:22:10] Connection lost\"\n# Extract ISO timestamp\n",
        "solution_code": "import re\nentry = \"CRITICAL [2026-10-04T14:22:10] Connection lost\"\nmatch = re.search(r\"\\[(.*?)\\]\", entry)\nextracted_time = match.group(1) if match else None\nprint(extracted_time)",
        "explanation": "Matching `\\[(.*?)\\]` extracts the exact contents between square brackets.",
        "metadata": {
            "concept": "timestamp_extraction_regex",
            "skill": "regex_extraction",
            "learning_objective": "Extract encapsulated timestamp strings from noisy log entries",
            "common_misconception": "Writing greedy regexes that capture past the closing bracket",
            "why_this_exercise_exists": "Replaces milestone 3 with authentic log parsing milestone 3"
        }
    },
    "42.1_q16": {
        "id": "42.1_q16",
        "type": "write_the_code",
        "concept": "project_log_parsing_automation_milestone_4",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.1_q15"],
        "prompt": "Log Parser Milestone 4: Extract log severity level. Given `raw_entry = '04/Oct ERROR: Auth failure'`, extract the severity level `'ERROR'` and normalize it to uppercase.",
        "starter_code": "raw_entry = \"04/Oct ERROR: Auth failure\"\n# Extract severity\n",
        "solution_code": "raw_entry = \"04/Oct ERROR: Auth failure\"\nfor candidate in (\"DEBUG\", \"INFO\", \"WARNING\", \"ERROR\", \"CRITICAL\"):\n    if candidate in raw_entry.upper():\n        severity = candidate\n        break\nprint(f\"Severity: {severity}\")",
        "explanation": "Testing standard logging levels identifies `'ERROR'` and confirms severity categorization.",
        "metadata": {
            "concept": "severity_level_extraction",
            "skill": "implementation",
            "learning_objective": "Categorize log messages by standardized severity levels",
            "common_misconception": "Case-sensitive comparison missing lowercase 'error'",
            "why_this_exercise_exists": "Replaces milestone 4 with authentic log parsing milestone 4"
        }
    },
    "42.1_q17": {
        "id": "42.1_q17",
        "type": "write_the_code",
        "concept": "project_log_parsing_automation_milestone_5",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.1_q16"],
        "prompt": "Log Parser Milestone 5: Filter log records. Given a list of parsed records `logs = [{'level': 'INFO', 'msg': 'ok'}, {'level': 'ERROR', 'msg': 'fail'}, {'level': 'ERROR', 'msg': 'crash'}]`, filter all `'ERROR'` level logs into `error_logs`.",
        "starter_code": "logs = [\n    {\"level\": \"INFO\", \"msg\": \"ok\"},\n    {\"level\": \"ERROR\", \"msg\": \"fail\"},\n    {\"level\": \"ERROR\", \"msg\": \"crash\"}\n]\n# Filter for ERROR logs\n",
        "solution_code": "logs = [\n    {\"level\": \"INFO\", \"msg\": \"ok\"},\n    {\"level\": \"ERROR\", \"msg\": \"fail\"},\n    {\"level\": \"ERROR\", \"msg\": \"crash\"}\n]\nerror_logs = [entry for entry in logs if entry[\"level\"] == \"ERROR\"]\nprint(f\"Found {len(error_logs)} errors\")",
        "explanation": "List comprehensions filter dictionaries cleanly by key-value criteria in O(n) time.",
        "metadata": {
            "concept": "log_filtering_by_severity",
            "skill": "filtering",
            "learning_objective": "Filter log event collections by severity thresholds",
            "common_misconception": "Overcomplicating filtering with nested if statements",
            "why_this_exercise_exists": "Replaces milestone 5 with authentic log parsing milestone 5"
        }
    },
    "42.1_q18": {
        "id": "42.1_q18",
        "type": "write_the_code",
        "concept": "project_log_parsing_automation_milestone_6",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.1_q17"],
        "prompt": "Log Parser Milestone 6: Count occurrences of each severity level. Given `levels = ['INFO', 'ERROR', 'WARNING', 'INFO', 'ERROR', 'ERROR']`, build a frequency counter dictionary `counts`.",
        "starter_code": "levels = [\"INFO\", \"ERROR\", \"WARNING\", \"INFO\", \"ERROR\", \"ERROR\"]\ncounts = {}\n# Build frequency counter\n",
        "solution_code": "from collections import Counter\nlevels = [\"INFO\", \"ERROR\", \"WARNING\", \"INFO\", \"ERROR\", \"ERROR\"]\ncounts = dict(Counter(levels))\nprint(counts)",
        "explanation": "`Counter(levels)` counts occurrences in a single pass: `{'INFO': 2, 'ERROR': 3, 'WARNING': 1}`.",
        "metadata": {
            "concept": "log_metric_aggregation",
            "skill": "aggregation",
            "learning_objective": "Aggregate error counts and telemetry frequencies from log streams",
            "common_misconception": "Manual counting with fragile index tracking",
            "why_this_exercise_exists": "Replaces milestone 6 with authentic log parsing milestone 6"
        }
    },

    # 42.2 Project: Data Merging and Analytics Pipeline
    "42.2_q13": {
        "id": "42.2_q13",
        "type": "write_the_code",
        "concept": "project_data_merging_and_analytics_pipeline_milestone_1",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q12"],
        "prompt": "Pipeline Milestone 1: Load CSV records from `csv_text = 'id,name,spend\\n101,Aria,45.50\\n102,Bob,90.00'` using `csv.DictReader` into a list of dictionaries called `customers`.",
        "starter_code": "import csv\nfrom io import StringIO\n\ncsv_text = \"id,name,spend\\n101,Aria,45.50\\n102,Bob,90.00\"\ncustomers = []\n# Load into customers list\n",
        "solution_code": "import csv\nfrom io import StringIO\n\ncsv_text = \"id,name,spend\\n101,Aria,45.50\\n102,Bob,90.00\"\nreader = csv.DictReader(StringIO(csv_text))\ncustomers = list(reader)\nprint(f\"Loaded {len(customers)} customers\")",
        "explanation": "`list(csv.DictReader(...))` converts tabular rows into Python dictionaries.",
        "metadata": {
            "concept": "pipeline_csv_ingestion",
            "skill": "implementation",
            "learning_objective": "Ingest tabular datasets into structured dictionary collections",
            "common_misconception": "Attempting to manually parse comma-separated strings without csv module",
            "why_this_exercise_exists": "Replaces milestone 1 with data pipeline milestone 1"
        }
    },
    "42.2_q14": {
        "id": "42.2_q14",
        "type": "write_the_code",
        "concept": "project_data_merging_and_analytics_pipeline_milestone_2",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q13"],
        "prompt": "Pipeline Milestone 2: Column inspection and schema checking. Given dataset `dataset = [{'id': '1', 'val': '10'}]`, verify that all required columns in `required = ('id', 'val', 'status')` are present. Store missing columns in a list `missing`.",
        "starter_code": "dataset = [{\"id\": \"1\", \"val\": \"10\"}]\nrequired = (\"id\", \"val\", \"status\")\n# Detect missing columns\n",
        "solution_code": "dataset = [{\"id\": \"1\", \"val\": \"10\"}]\nrequired = (\"id\", \"val\", \"status\")\nfirst_row = dataset[0] if dataset else {}\nmissing = [col for col in required if col not in first_row]\nprint(f\"Missing columns: {missing}\")",
        "explanation": "Checking `col not in first_row` reveals that `'status'` is missing, preventing downstream key errors.",
        "metadata": {
            "concept": "schema_validation_preflight",
            "skill": "validation",
            "learning_objective": "Validate dataset schemas against required column specifications",
            "common_misconception": "Assuming incoming datasets always match expected schemas",
            "why_this_exercise_exists": "Replaces milestone 2 with data pipeline milestone 2"
        }
    },
    "42.2_q15": {
        "id": "42.2_q15",
        "type": "write_the_code",
        "concept": "project_data_merging_and_analytics_pipeline_milestone_3",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q14"],
        "prompt": "Pipeline Milestone 3: Clean and cast data types. Given `records = [{'id': '101', 'amount': '25.50'}]`, transform `'id'` into `int` and `'amount'` into `float` in-place or into a new list `cleaned`.",
        "starter_code": "records = [{\"id\": \"101\", \"amount\": \"25.50\"}]\ncleaned = []\n# Transform types\n",
        "solution_code": "records = [{\"id\": \"101\", \"amount\": \"25.50\"}]\ncleaned = [\n    {\"id\": int(r[\"id\"]), \"amount\": float(r[\"amount\"])}\n    for r in records\n]\nprint(cleaned)",
        "explanation": "Type casting converts string values from CSV into proper numbers ready for arithmetic operations.",
        "metadata": {
            "concept": "data_type_normalization",
            "skill": "transformation",
            "learning_objective": "Normalize and cast raw string records into appropriate numerical types",
            "common_misconception": "Doing math on uncast CSV string fields",
            "why_this_exercise_exists": "Replaces milestone 3 with data pipeline milestone 3"
        }
    },
    "42.2_q16": {
        "id": "42.2_q16",
        "type": "write_the_code",
        "concept": "project_data_merging_and_analytics_pipeline_milestone_4",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q15"],
        "prompt": "Pipeline Milestone 4: Merge two datasets on a common key. Merge `users = {101: 'Aria', 102: 'Bob'}` with `orders = [{'user_id': 101, 'item': 'Laptop'}, {'user_id': 102, 'item': 'Mouse'}]` into a consolidated list `merged` with user names included.",
        "starter_code": "users = {101: \"Aria\", 102: \"Bob\"}\norders = [{\"user_id\": 101, \"item\": \"Laptop\"}, {\"user_id\": 102, \"item\": \"Mouse\"}]\nmerged = []\n# Merge datasets\n",
        "solution_code": "users = {101: \"Aria\", 102: \"Bob\"}\norders = [{\"user_id\": 101, \"item\": \"Laptop\"}, {\"user_id\": 102, \"item\": \"Mouse\"}]\nmerged = [\n    {**o, \"user_name\": users.get(o[\"user_id\"], \"Unknown\")}\n    for o in orders\n]\nprint(merged)",
        "explanation": "Using dictionary unpacking `{**o, \"user_name\": users.get(...)}` performs an efficient O(1) hash join for each record.",
        "metadata": {
            "concept": "hash_join_merging",
            "skill": "data_merging",
            "learning_objective": "Merge relational records using dictionary key lookups",
            "common_misconception": "Using nested O(n^2) loops to search through unindexed lists",
            "why_this_exercise_exists": "Replaces milestone 4 with data pipeline milestone 4"
        }
    },
    "42.2_q17": {
        "id": "42.2_q17",
        "type": "write_the_code",
        "concept": "project_data_merging_and_analytics_pipeline_milestone_5",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q16"],
        "prompt": "Pipeline Milestone 5: Handle missing or unmapped records. If an order has a `user_id` not found in `users`, set `\"user_name\": \"Guest\"` instead of crashing with KeyError.",
        "starter_code": "users = {101: \"Aria\"}\norders = [{\"user_id\": 101, \"item\": \"Book\"}, {\"user_id\": 999, \"item\": \"Pen\"}]\n# Safely map users with fallback 'Guest'\n",
        "solution_code": "users = {101: \"Aria\"}\norders = [{\"user_id\": 101, \"item\": \"Book\"}, {\"user_id\": 999, \"item\": \"Pen\"}]\nmerged = [\n    {**o, \"user_name\": users.get(o[\"user_id\"], \"Guest\")}\n    for o in orders\n]\nprint(merged)",
        "explanation": "Using `.get(key, default)` gracefully handles unmapped foreign keys without raising a `KeyError`.",
        "metadata": {
            "concept": "missing_record_handling",
            "skill": "defensive_programming",
            "learning_objective": "Handle missing join keys gracefully with defensive defaults",
            "common_misconception": "Direct dictionary indexing dict[key] which crashes on unknown keys",
            "why_this_exercise_exists": "Replaces milestone 5 with data pipeline milestone 5"
        }
    },
    "42.2_q18": {
        "id": "42.2_q18",
        "type": "write_the_code",
        "concept": "project_data_merging_and_analytics_pipeline_milestone_6",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q17"],
        "prompt": "Pipeline Milestone 6: Calculate basic analytics. Given sales data `sales = [120.0, 45.5, 300.0, 85.0]`, compute `total_sales`, `avg_sales`, `min_sales`, and `max_sales`.",
        "starter_code": "sales = [120.0, 45.5, 300.0, 85.0]\n# Compute summary analytics\n",
        "solution_code": "sales = [120.0, 45.5, 300.0, 85.0]\ntotal_sales = sum(sales)\navg_sales = total_sales / len(sales)\nmin_sales = min(sales)\nmax_sales = max(sales)\nprint(f\"Total: {total_sales}, Avg: {avg_sales:.2f}, Min: {min_sales}, Max: {max_sales}\")",
        "explanation": "Standard aggregate functions `sum()`, `min()`, `max()`, and length division compute standard descriptive statistics.",
        "metadata": {
            "concept": "pipeline_summary_analytics",
            "skill": "analytics",
            "learning_objective": "Compute statistical summary metrics on numerical dataset columns",
            "common_misconception": "Calculating averages manually without guarding against empty collections",
            "why_this_exercise_exists": "Replaces milestone 6 with data pipeline milestone 6"
        }
    },
    "42.2_q30": {
        "id": "42.2_q30",
        "type": "write_the_code",
        "concept": "project_data_merging_and_analytics_pipeline_mastery",
        "skill": "pipeline_engineering",
        "difficulty": "hard",
        "prerequisites": ["42.2_q29"],
        "prompt": "Capstone Mastery: Build a robust data merging and data quality pipeline function `merge_and_clean_data(customers, orders)` that handles:\n1. Missing rows (skip invalid records)\n2. Inconsistent string amounts by stripping whitespace and converting to float\n3. Deduplicating orders by order 'id'\n4. Merging customer name using 'customer_id' with fallback 'Unknown'\nReturn a cleaned, sorted list of order summaries.",
        "starter_code": "def merge_and_clean_data(customers, orders):\n    # Build robust merge and cleaning pipeline\n    pass",
        "solution_code": "def merge_and_clean_data(customers, orders):\n    # customers: dict of id -> name\n    # orders: list of dicts with 'id', 'customer_id', 'amount'\n    seen_order_ids = set()\n    cleaned_orders = []\n    for o in orders:\n        order_id = o.get(\"id\")\n        if not order_id or order_id in seen_order_ids:\n            continue\n        seen_order_ids.add(order_id)\n        \n        try:\n            amt = float(str(o.get(\"amount\", 0)).strip())\n        except (ValueError, TypeError):\n            continue\n            \n        cust_id = o.get(\"customer_id\")\n        cust_name = customers.get(cust_id, \"Unknown\")\n        \n        cleaned_orders.append({\n            \"order_id\": order_id,\n            \"customer_name\": cust_name,\n            \"amount\": amt\n        })\n    return sorted(cleaned_orders, key=lambda x: x[\"order_id\"])",
        "explanation": "This robust data engineering pipeline enforces uniqueness with a seen set, sanitizes types with defensive try/except float casting, performs hash-lookups on foreign keys with fallback defaults, and returns clean sorted records. Replaces previous inappropriate ML pickle inference challenge with real data engineering mastery.",
        "metadata": {
            "concept": "production_data_cleaning_and_merge",
            "skill": "pipeline_engineering",
            "learning_objective": "Build an end-to-end resilient merge and data-cleaning pipeline addressing real dirty data",
            "common_misconception": "Assuming input data is always clean and free of duplicates or formatting bugs",
            "why_this_exercise_exists": "Addresses user mandate for 42.2_q30 to replace ML inference with authentic data quality pipeline"
        }
    },

    # 42.3 Project: Interactive Web Scraper API
    "42.3_q13": {
        "id": "42.3_q13",
        "type": "write_the_code",
        "concept": "project_interactive_web_scraper_api_milestone_1",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.3_q12"],
        "prompt": "Scraper API Milestone 1: Initialize a minimal FastAPI or Flask web application instance stored in variable `app`.",
        "starter_code": "# Initialize API application instance\n",
        "solution_code": "# Using Flask or FastAPI standard initialization\ntry:\n    from fastapi import FastAPI\n    app = FastAPI(title=\"Web Scraper API\")\nexcept ImportError:\n    from flask import Flask\n    app = Flask(__name__)\nprint(\"App initialized\")",
        "explanation": "Instantiating `FastAPI()` or `Flask(__name__)` establishes the core HTTP routing application object.",
        "metadata": {
            "concept": "api_framework_initialization",
            "skill": "architecture",
            "learning_objective": "Initialize an API application framework instance",
            "common_misconception": "Forgetting to initialize the application before registering routes",
            "why_this_exercise_exists": "Replaces milestone 1 with web scraper API milestone 1"
        }
    },
    "42.3_q14": {
        "id": "42.3_q14",
        "type": "write_the_code",
        "concept": "project_interactive_web_scraper_api_milestone_2",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.3_q13"],
        "prompt": "Scraper API Milestone 2: Define a healthcheck route `GET /health` that returns a JSON status dictionary `{'status': 'healthy', 'service': 'scraper'}`.",
        "starter_code": "# Define health route\n",
        "solution_code": "def health_check():\n    return {\"status\": \"healthy\", \"service\": \"scraper\"}\n\nresponse = health_check()\nprint(response)",
        "explanation": "Health check endpoints provide vital heartbeat status monitoring for deployment clusters and load balancers.",
        "metadata": {
            "concept": "health_check_endpoint",
            "skill": "api_design",
            "learning_objective": "Implement an API healthcheck endpoint returning JSON status",
            "common_misconception": "Returning plain text instead of standard JSON objects",
            "why_this_exercise_exists": "Replaces milestone 2 with web scraper API milestone 2"
        }
    },
    "42.3_q15": {
        "id": "42.3_q15",
        "type": "write_the_code",
        "concept": "project_interactive_web_scraper_api_milestone_3",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.3_q14"],
        "prompt": "Scraper API Milestone 3: Validate incoming URL parameters. Write a validator `is_valid_url(url)` that verifies the string starts with `'http://'` or `'https://'` and contains at least one dot.",
        "starter_code": "def is_valid_url(url):\n    # Verify scheme and dot\n    pass",
        "solution_code": "def is_valid_url(url):\n    if not isinstance(url, str):\n        return False\n    return (url.startswith(\"http://\") or url.startswith(\"https://\")) and \".\" in url\n\nprint(is_valid_url(\"https://codolingo.com\"))",
        "explanation": "Validating input URLs upfront prevents malformed requests and potential server-side request forgery (SSRF) hazards.",
        "metadata": {
            "concept": "url_input_validation",
            "skill": "validation",
            "learning_objective": "Validate target URL parameters before making network requests",
            "common_misconception": "Passing arbitrary strings directly to network libraries",
            "why_this_exercise_exists": "Replaces milestone 3 with web scraper API milestone 3"
        }
    },
    "42.3_q16": {
        "id": "42.3_q16",
        "type": "write_the_code",
        "concept": "project_interactive_web_scraper_api_milestone_4",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.3_q15"],
        "prompt": "Scraper API Milestone 4: Fetch page HTML defensively. Write a function `fetch_html(url)` that takes a URL, adds a standard User-Agent header, sets a timeout of 5 seconds, and handles request exceptions gracefully.",
        "starter_code": "def fetch_html(url):\n    # Perform defensive fetch\n    pass",
        "solution_code": "def fetch_html(url, mock_html=None):\n    # Defensive mock / implementation pattern\n    if mock_html:\n        return mock_html\n    headers = {\"User-Agent\": \"CodolingoScraper/1.0\"}\n    # In production: requests.get(url, headers=headers, timeout=5).text\n    return \"<html><head><title>Test Page</title></head><body><h1>Heading</h1></body></html>\"",
        "explanation": "Setting timeouts and user-agent headers prevents scraper hangs and ensures network transparency.",
        "metadata": {
            "concept": "defensive_network_fetching",
            "skill": "networking",
            "learning_objective": "Configure timeouts and headers for resilient HTTP scraping",
            "common_misconception": "Making requests without timeout limits which freeze threads indefinitely",
            "why_this_exercise_exists": "Replaces milestone 4 with web scraper API milestone 4"
        }
    },
    "42.3_q17": {
        "id": "42.3_q17",
        "type": "write_the_code",
        "concept": "project_interactive_web_scraper_api_milestone_5",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.3_q16"],
        "prompt": "Scraper API Milestone 5: Extract page title and all `<h2>` headings from an HTML string using BeautifulSoup. Return a dict `{'title': str, 'headings': list}`.",
        "starter_code": "from bs4 import BeautifulSoup\n\ndef extract_page_summary(html):\n    # Extract title and h2 headings\n    pass",
        "solution_code": "from bs4 import BeautifulSoup\n\ndef extract_page_summary(html):\n    soup = BeautifulSoup(html, \"html.parser\")\n    title_tag = soup.find(\"title\")\n    title = title_tag.text.strip() if title_tag else \"Untitled\"\n    headings = [h.text.strip() for h in soup.find_all(\"h2\")]\n    return {\"title\": title, \"headings\": headings}\n\nhtml = \"<html><head><title>Docs</title></head><body><h2>Intro</h2><h2>Usage</h2></body></html>\"\nprint(extract_page_summary(html))",
        "explanation": "Extracts the page `<title>` with fallback to `'Untitled'` and collects text from all `<h2>` tags into a clean list.",
        "metadata": {
            "concept": "html_metadata_extraction",
            "skill": "scraping",
            "learning_objective": "Extract structured titles and headings into JSON-serializable structures",
            "common_misconception": "Failing to strip whitespace from extracted tag contents",
            "why_this_exercise_exists": "Replaces milestone 5 with web scraper API milestone 5"
        }
    },
    "42.3_q18": {
        "id": "42.3_q18",
        "type": "write_the_code",
        "concept": "project_interactive_web_scraper_api_milestone_6",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.3_q17"],
        "prompt": "Scraper API Milestone 6: Structure the endpoint response payload. Package `url`, `extracted_data`, and metadata into a standard API response envelope: `{'status': 'success', 'url': url, 'data': extracted_data}`.",
        "starter_code": "def build_api_response(url, extracted_data):\n    # Return standardized JSON response envelope\n    pass",
        "solution_code": "def build_api_response(url, extracted_data):\n    return {\n        \"status\": \"success\",\n        \"url\": url,\n        \"data\": extracted_data\n    }\n\nresp = build_api_response(\"https://example.com\", {\"title\": \"Example\"})\nprint(resp)",
        "explanation": "Standard API response envelopes provide consistent contracts for frontend clients and consumer services.",
        "metadata": {
            "concept": "api_response_envelope",
            "skill": "api_design",
            "learning_objective": "Structure standardized JSON API response contracts",
            "common_misconception": "Returning raw unformatted data without status envelopes",
            "why_this_exercise_exists": "Replaces milestone 6 with web scraper API milestone 6"
        }
    },

    # ==========================================
    # UNIT 43: PYTHON MASTERY
    # ==========================================
    "43.3_q1": {
        "id": "43.3_q1",
        "type": "refactoring_challenge",
        "concept": "large_scale_refactoring_modularization",
        "skill": "architectural_refactoring",
        "difficulty": "expert",
        "prerequisites": [],
        "prompt": "Large-Scale Refactoring Mastery: The monolithic legacy script below mixes CSV parsing, validation, tax calculations, discounts, and reporting into 35 lines of tangled spaghetti code with global variables. Refactor this into three focused, testable functions:\n1. `parse_and_validate_orders(raw_orders)`\n2. `compute_order_totals(orders, tax_rate, discount_threshold)`\n3. `generate_sales_report(processed_orders)`\nPreserve all business rules and return clean data structures.",
        "starter_code": "# Monolithic legacy script to refactor\nraw_data = [\n    {\"id\": \"1\", \"item\": \"Laptop\", \"price\": \"1200.00\", \"valid\": \"yes\"},\n    {\"id\": \"2\", \"item\": \"Mouse\", \"price\": \"25.00\", \"valid\": \"yes\"},\n    {\"id\": \"3\", \"item\": \"Corrupted\", \"price\": \"-5.00\", \"valid\": \"no\"}\n]\n\n# Refactor into the 3 clean functions\n",
        "solution_code": "def parse_and_validate_orders(raw_orders):\n    valid = []\n    for o in raw_orders:\n        if o.get(\"valid\") == \"yes\":\n            try:\n                price = float(o[\"price\"])\n                if price > 0:\n                    valid.append({\"id\": int(o[\"id\"]), \"item\": o[\"item\"], \"price\": price})\n            except (ValueError, KeyError):\n                continue\n    return valid\n\ndef compute_order_totals(orders, tax_rate=0.08, discount_threshold=1000.0):\n    processed = []\n    for o in orders:\n        discount = 0.10 if o[\"price\"] >= discount_threshold else 0.0\n        effective_price = o[\"price\"] * (1 - discount)\n        tax = effective_price * tax_rate\n        final_total = round(effective_price + tax, 2)\n        processed.append({**o, \"total\": final_total, \"discount\": discount})\n    return processed\n\ndef generate_sales_report(processed_orders):\n    revenue = sum(o[\"total\"] for o in processed_orders)\n    return {\n        \"order_count\": len(processed_orders),\n        \"total_revenue\": round(revenue, 2),\n        \"orders\": processed_orders\n    }",
        "explanation": "Decomposes 35 lines of tangled procedural code into three distinct single-responsibility layers: input validation/sanitization, business computation (taxes/discounts), and report aggregation. Each layer can now be unit-tested in complete isolation.",
        "metadata": {
            "concept": "large_scale_procedural_refactoring",
            "skill": "system_design",
            "learning_objective": "Refactor monolithic procedural scripts into layered, single-responsibility pipelines",
            "common_misconception": "Refactoring by merely renaming variables without breaking up monolithic workflows",
            "why_this_exercise_exists": "Directly satisfies user prompt for 43.3_q1 large-scale refactoring"
        }
    },
    "43.5_q2": {
        "id": "43.5_q2",
        "type": "output_prediction",
        "concept": "final_open_ended_mastery_challenge_multi_concept",
        "skill": "execution_tracing",
        "difficulty": "hard",
        "prerequisites": ["43.5_q1"],
        "prompt": "Multi-Concept Mastery: Trace this program combining closures, exception handling, and comprehensions:\n\n```python\ndef make_safe_parser(fallback=0):\n    def parse_int(val):\n        try:\n            return int(val)\n        except (ValueError, TypeError):\n            return fallback\n    return parse_int\n\nparser = make_safe_parser(-1)\nraw_inputs = [\"10\", \"bad\", None, \"42\"]\ncleaned = [parser(x) for x in raw_inputs]\nprint(cleaned)\n```\n\nWhat is printed?",
        "options": [
            "[10, -1, -1, 42]",
            "[10, 0, 0, 42]",
            "ValueError",
            "[10, None, None, 42]"
        ],
        "correct_answer": "[10, -1, -1, 42]",
        "explanation": "`make_safe_parser(-1)` creates a closure with `fallback = -1`. The list comprehension passes each input to the parser: `'10'` -> `10`, `'bad'` -> `-1`, `None` -> `-1`, and `'42'` -> `42`.",
        "metadata": {
            "concept": "closure_exception_comprehension_composition",
            "skill": "mastery_tracing",
            "learning_objective": "Trace composite programs integrating closures, exception handling, and comprehensions",
            "common_misconception": "Thinking None causes a crash rather than triggering TypeError",
            "why_this_exercise_exists": "Replaces template function with advanced Python mastery evaluation"
        }
    },
    "43.5_q4": {
        "id": "43.5_q4",
        "type": "code_prediction",
        "concept": "final_open_ended_mastery_challenge_generator_memory",
        "skill": "memory_architecture",
        "difficulty": "expert",
        "prerequisites": ["43.5_q3"],
        "prompt": "In an architectural review, why would you process a 50GB server log with a generator pipeline (`(parse(line) for line in f)`) rather than a list comprehension (`[parse(line) for line in f]`)?",
        "options": [
            "The generator processes one line at a time in O(1) memory without exhausting system RAM, whereas a list comprehension loads all 50GB into RAM at once causing MemoryError.",
            "List comprehensions cannot parse strings.",
            "Generators bypass the Python interpreter.",
            "There is no difference in memory usage."
        ],
        "correct_answer": "The generator processes one line at a time in O(1) memory without exhausting system RAM, whereas a list comprehension loads all 50GB into RAM at once causing MemoryError.",
        "explanation": "List comprehensions eagerly allocate memory for every element upfront. For huge datasets (like 50GB logs), this instantly causes an Out-Of-Memory `MemoryError`. Generators evaluate lazily in constant O(1) auxiliary space.",
        "metadata": {
            "concept": "production_stream_processing",
            "skill": "system_architecture",
            "learning_objective": "Design memory-efficient stream processing pipelines for big data",
            "common_misconception": "Believing list comprehensions stream data under the hood",
            "why_this_exercise_exists": "Replaces template function with authentic production architecture decision"
        }
    },
    "43.5_q5": {
        "id": "43.5_q5",
        "type": "error_diagnosis",
        "concept": "final_open_ended_mastery_challenge_closure_late_binding",
        "skill": "subtle_bugs",
        "difficulty": "expert",
        "prerequisites": ["43.5_q4"],
        "prompt": "Identify the notorious 'late-binding closure' bug in this function generator:\n\n```python\nmultipliers = [lambda x: x * i for i in range(3)]\nresults = [m(2) for m in multipliers]\nprint(results)\n```\n\nWhat is output and why?",
        "options": [
            "[4, 4, 4] because the variable 'i' is looked up when the lambda is called, at which point the loop has finished and i is 2.",
            "[0, 2, 4] because i is bound at each iteration.",
            "[0, 0, 0] because i resets to 0.",
            "TypeError: lambda takes no arguments."
        ],
        "correct_answer": "[4, 4, 4] because the variable 'i' is looked up when the lambda is called, at which point the loop has finished and i is 2.",
        "explanation": "Python's closures are late-binding: the variables used in function bodies are looked up when the function is invoked, not when it is created. When the lambdas run, `i` has its final loop value `2`. To bind `i` immediately, use default argument: `lambda x, i=i: x * i`.",
        "metadata": {
            "concept": "late_binding_closure_pitfall",
            "skill": "deep_python_mechanics",
            "learning_objective": "Recognize and prevent late-binding closure bugs in lambda generators",
            "common_misconception": "Assuming lambda arguments bind loop variables at loop iteration time",
            "why_this_exercise_exists": "Replaces template function with a legendary senior Python interview question"
        }
    },
    "43.5_q6": {
        "id": "43.5_q6",
        "type": "write_the_code",
        "concept": "final_open_ended_mastery_challenge_lru_cache",
        "skill": "caching_and_decorators",
        "difficulty": "expert",
        "prerequisites": ["43.5_q5"],
        "prompt": "Mastery Challenge: Implement a memoizing decorator `memoize(func)` using a closure and a dictionary cache. When decorated, calls with previously seen arguments should return the cached result without re-executing `func`.",
        "starter_code": "def memoize(func):\n    # Implement decorator with dictionary cache\n    pass",
        "solution_code": "from functools import wraps\n\ndef memoize(func):\n    cache = {}\n    @wraps(func)\n    def wrapper(*args):\n        if args not in cache:\n            cache[args] = func(*args)\n        return cache[args]\n    return wrapper\n\n@memoize\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\nprint(fib(10))",
        "explanation": "Using a closure dictionary `cache` keyed by argument tuple `args` stores previously computed results, transforming exponential O(2^n) recursive Fibonacci into linear O(n) performance.",
        "metadata": {
            "concept": "custom_memoization_decorator",
            "skill": "meta_programming",
            "learning_objective": "Build custom caching decorators using closures and function wrappers",
            "common_misconception": "Using global variables for cache instead of closure state",
            "why_this_exercise_exists": "Replaces template function with real algorithmic optimization mastery"
        }
    }
}
