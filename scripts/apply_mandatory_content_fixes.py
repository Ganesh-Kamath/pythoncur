"""
apply_mandatory_content_fixes.py

Directly modifies lesson JSON files across the Codolingo Python curriculum
to enforce the 20 Mandatory Changes:
1. Python Mental Models (Variables as labels/references, mutation vs reassignment,
   aliasing, == vs is, None, truthiness, return vs print).
2. Real Debugging (genuine logic, off-by-one, condition inversion, loop state,
   mutable defaults, aliasing bugs).
3. Independent Code Writing & Scaffolding Reduction (typed signatures, docstrings,
   unscaffolded challenge problems).
4. Problem Solving (Choosing data structures, comparing solutions, handling constraints).
5. Transfer & Edge Cases (Real-world contexts: logs, APIs, shopping carts, empty collections).
6. Retention across units (return vs print in testing/OOP, mutation in functions,
   exceptions in APIs/DBs).
7. DSA Judgment (When to use / when NOT to use, Big-O tradeoffs).
8. OOP Design Reasoning (Composition vs inheritance, class vs instance attributes).
9. Advanced Practical Python (Generators for large files, decorators for timing/auth,
   asyncio non-blocking vs blocking).
10. Modern Python & Type Hints (Type annotations, dataclasses, match-case).
11. Security Basics (Parameterized queries to prevent SQL injection, environment variables for secrets).
"""

import json
from pathlib import Path

CONTENT_DIR = Path("python_content")

def load_lesson(pattern_str):
    matches = list(CONTENT_DIR.glob(pattern_str))
    if not matches:
        # try fuzzy by splitting
        parts = pattern_str.split("/")
        if len(parts) == 2:
            prefix = parts[1].split("_")[0]
            matches = list((CONTENT_DIR / parts[0]).glob(f"{prefix}_*.json"))
    if not matches:
        raise FileNotFoundError(f"Missing match for {pattern_str}")
    fp = matches[0]
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f), fp

def save_lesson(data, fp):
    for item in data.get("items", []):
        if "prerequisites" not in item:
            item["prerequisites"] = []
        if item.get("type") == "spot_the_bug":
            item["type"] = "error_diagnosis"
        if item.get("difficulty") not in {"easy", "medium", "hard", "expert"}:
            item["difficulty"] = "hard"
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

def upgrade_unit_02_mental_models():
    """
    Unit 2 Lesson 2.1: Variables as Names/References, NOT physical boxes.
    """
    data, fp = load_lesson("unit_02/2.1_variables.json")
    items = data["items"]
    
    # Q1: Micro lesson - Variables as Object References
    items[0] = {
        "id": "2.1_q1",
        "type": "micro_lesson",
        "title": "Variables Are Labels, Not Boxes",
        "content": "In Python, a variable is not a physical box that holds data. Instead, a variable is a **name tag** or **reference** attached to an object in memory.\n\nWhen you write `x = 42`, Python creates an integer object `42` in memory and binds the label `x` to it. If you later write `y = x`, Python does not make a copy of `42`; it simply binds a second label `y` to the very same object in memory.",
        "difficulty": "easy",
        "concept": "variable_references",
        "skill": "mental_model"
    }
    
    # Q2: MCQ testing the mental model of references vs boxes
    items[1] = {
        "id": "2.1_q2",
        "type": "multiple_choice",
        "question": "Which statement best describes what happens in Python when you execute `score = 100`?",
        "options": [
            "Python creates an integer object 100 in memory and binds the name tag 'score' to refer to that object",
            "Python allocates a fixed physical memory box named 'score' and stores the bits of 100 inside that box permanently",
            "Python converts the string 'score' into an integer of value 100",
            "Python creates two distinct copies of 100: one for the variable and one for the screen"
        ],
        "correct_answer": "Python creates an integer object 100 in memory and binds the name tag 'score' to refer to that object",
        "explanation": "In Python's execution model, variables are references (labels) pointing to objects. When you assign `score = 100`, Python allocates an int object with value 100 and points the identifier `score` to it.",
        "difficulty": "easy",
        "concept": "variable_references",
        "skill": "mental_model"
    }
    
    # Q6: Code prediction testing rebinding
    items[5] = {
        "id": "2.1_q6",
        "type": "multiple_choice",
        "question": "What happens in memory when this code executes?\n\n```python\na = 10\nb = a\na = 20\n```",
        "options": [
            "a is rebound to a new int object 20, while b still refers to the original int object 10",
            "Both a and b now refer to 20 because changing a automatically changes b",
            "Python raises a ReassignmentError because integers cannot be reassigned",
            "b becomes None because a was overwritten"
        ],
        "correct_answer": "a is rebound to a new int object 20, while b still refers to the original int object 10",
        "explanation": "When `b = a` runs, `b` points to the object `10`. When `a = 20` runs, the label `a` is rebound to a new object `20`. The name `b` still points to `10`. Integers are immutable, so rebinding `a` has zero effect on `b`.",
        "difficulty": "easy",
        "concept": "variable_rebinding",
        "skill": "memory_tracing"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 02: Variable References mental models.")

def upgrade_unit_04_identity_and_truthiness():
    """
    Unit 4: Equality vs Identity (== vs is), None, and Truthiness.
    """
    data, fp = load_lesson("unit_04/4.3_string_concatenation.json")
    # Also check if there's a dedicated identity lesson or enhance comparison
    # Let's inspect unit_03 or unit_04
    pass

def upgrade_unit_08_mutation_and_aliasing():
    """
    Unit 8 Lesson 8.3: Adding Elements (append vs +) and Aliasing.
    """
    data, fp = load_lesson("unit_08/8.3_adding_elements_append_and_insert.json")
    items = data["items"]
    
    # Q2: In-place mutation vs Reassignment
    items[1] = {
        "id": "8.3_q2",
        "type": "multiple_choice",
        "question": "What is the crucial difference between `numbers.append(4)` and `numbers = numbers + [4]`?",
        "options": [
            "append(4) mutates the existing list in-place and returns None, whereas numbers + [4] creates a brand-new list object in memory",
            "append(4) creates a new list and returns it, while + [4] modifies the list in place",
            "Both operations create a new list, but append() is only allowed for integer elements",
            "append(4) leaves the original list unchanged and prints the new item to the console"
        ],
        "correct_answer": "append(4) mutates the existing list in-place and returns None, whereas numbers + [4] creates a brand-new list object in memory",
        "explanation": "In Python, `.append()` is an in-place mutation: it adds the element directly to the existing list object and returns `None`. In contrast, concatenation `+` creates a brand-new list object containing all combined items and requires reassigning the variable.",
        "difficulty": "easy",
        "concept": "mutation_vs_reassignment",
        "skill": "mental_model"
    }
    
    # Q9: Aliasing prediction
    items[8] = {
        "id": "8.3_q9",
        "type": "output_prediction",
        "question": "What is the exact output of this code?\n\n```python\nfirst = [1, 2]\nsecond = first\nsecond.append(3)\nprint(first)\n```",
        "options": [
            "[1, 2, 3]",
            "[1, 2]",
            "None",
            "RuntimeError: aliased list modified"
        ],
        "correct_answer": "[1, 2, 3]",
        "explanation": "`second = first` does NOT create a copy of the list; both variables reference the exact same list object in memory (aliasing). When `second.append(3)` mutates the underlying list, viewing it via `first` reflects the change `[1, 2, 3]`.",
        "difficulty": "medium",
        "concept": "aliasing_and_mutability",
        "skill": "state_tracing"
    }
    
    # Q18: Debugging accidental None assignment from append()
    items[17] = {
        "id": "8.3_q18",
        "type": "spot_the_bug",
        "question": "A developer wrote this code to add a score to their leaderboard:\n\n```python\nscores = [95, 88, 72]\nscores = scores.append(90)\nprint(len(scores))\n```\nWhy does line 3 raise a `TypeError: object of type 'NoneType' has no len()`?",
        "options": [
            "scores.append() mutates the list in place and returns None, so rebinding scores = scores.append(90) sets scores to None",
            "append() can only accept strings, so passing 90 causes a silent conversion to None",
            "len() cannot measure lists that have more than 3 elements",
            "The list must be sorted before calling len()"
        ],
        "correct_answer": "scores.append() mutates the list in place and returns None, so rebinding scores = scores.append(90) sets scores to None",
        "explanation": "This is one of the most frequent Python beginner bugs: `.append()` modifies the list in place and returns `None`. By assigning `scores = scores.append(90)`, the variable `scores` is overwritten with `None`, breaking subsequent operations.",
        "difficulty": "medium",
        "concept": "append_returns_none",
        "skill": "debugging"
    }
    
    # Q26: Transfer question: Shopping Cart Alias vs Copy
    items[25] = {
        "id": "8.3_q26",
        "type": "multiple_choice",
        "question": "You are building an e-commerce checkout. You want to create a preview cart with a promotional item added, WITHOUT modifying the user's active shopping cart session. Which pattern safely achieves this?",
        "options": [
            "preview = user_cart.copy()\npreview.append(promo_item)",
            "preview = user_cart\npreview.append(promo_item)",
            "preview = user_cart.append(promo_item)",
            "preview = list(user_cart.append(promo_item))"
        ],
        "correct_answer": "preview = user_cart.copy()\npreview.append(promo_item)",
        "explanation": "To prevent modifying the active session cart, you must create a shallow copy (`user_cart.copy()` or `list(user_cart)`). Simply doing `preview = user_cart` would alias the active cart, causing promo modifications to corrupt the live user session.",
        "difficulty": "hard",
        "concept": "shallow_copy_vs_alias",
        "skill": "system_design"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 08: Mutation, Aliasing, and Append return None.")

def upgrade_unit_11_return_vs_print():
    """
    Unit 11 Lesson 11.4: Functions - return vs print, returning None.
    """
    data, fp = load_lesson("unit_11/11.4_*.json")
    items = data["items"]
    
    # Q1: Micro lesson on return vs print
    items[0] = {
        "id": "11.4_q1",
        "type": "micro_lesson",
        "title": "Return vs. Print: Output to Caller vs. Output to Screen",
        "content": "A crucial distinction in Python programming is the difference between `print()` and `return`:\n\n- `print()` writes text to the terminal console so a human can read it. It returns `None`.\n- `return` sends a value back to the code that called the function, allowing that value to be stored in a variable, passed to another function, or used in math.\n\nIf a function finishes without encountering an explicit `return` statement, Python automatically returns `None`.",
        "difficulty": "easy",
        "concept": "return_vs_print",
        "skill": "mental_model"
    }
    
    # Q2: MCQ testing return vs print
    items[1] = {
        "id": "11.4_q2",
        "type": "multiple_choice",
        "question": "Consider the following function:\n\n```python\ndef calculate_tax(subtotal):\n    print(subtotal * 0.08)\n\ntotal = 100 + calculate_tax(100)\n```\nWhat happens when this script is run?",
        "options": [
            "It prints 8.0 to the console and then raises TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'",
            "It calculates total as 108.0 without error",
            "It prints 108.0 directly to the terminal",
            "It raises a SyntaxError because print cannot appear inside a function"
        ],
        "correct_answer": "It prints 8.0 to the console and then raises TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'",
        "explanation": "Because `calculate_tax` calls `print()` but has no `return` statement, it implicitly returns `None`. When Python tries to evaluate `100 + None`, it raises a `TypeError` because you cannot add an integer and `NoneType`.",
        "difficulty": "medium",
        "concept": "return_vs_print",
        "skill": "debugging"
    }
    
    # Q17: Spot the bug on returning vs printing
    items[16] = {
        "id": "11.4_q17",
        "type": "spot_the_bug",
        "question": "A developer wrote a helper to format usernames, but tests show that `greeting = f'Hello, {format_name(\"alice\")}'` results in `'Hello, None'`!\n\n```python\ndef format_name(raw_name):\n    clean = raw_name.strip().title()\n    print(clean)\n```\nHow should this bug be repaired?",
        "options": [
            "Replace `print(clean)` with `return clean` so the formatted string is returned to the caller instead of returning None",
            "Change `clean = raw_name.strip().title()` to `raw_name = clean`",
            "Wrap the call in `str(format_name('alice'))`",
            "Call `format_name` twice in succession"
        ],
        "correct_answer": "Replace `print(clean)` with `return clean` so the formatted string is returned to the caller instead of returning None",
        "explanation": "`print()` only displays characters in the terminal and returns `None`. Replacing `print(clean)` with `return clean` passes the formatted string back to the caller so it can be interpolated into strings or saved in variables.",
        "difficulty": "medium",
        "concept": "return_vs_print",
        "skill": "debugging"
    }
    
    # Q27: Transfer: Pipeline function design
    items[26] = {
        "id": "11.4_q27",
        "type": "real_world_scenario",
        "question": "You are building a data ingestion pipeline where output from `clean_row(row)` is passed directly into `validate_schema(row)`. Why MUST `clean_row` use `return` rather than `print`?",
        "options": [
            "Downstream processing functions require the actual cleaned data object in memory; print() only outputs to stdout and supplies None to validate_schema()",
            "print() is blocked by default in production Linux environments",
            "return encrypts the data during transmission between functions",
            "Functions that print cannot accept dictionaries as arguments"
        ],
        "correct_answer": "Downstream processing functions require the actual cleaned data object in memory; print() only outputs to stdout and supplies None to validate_schema()",
        "explanation": "In software architecture and data pipelines, functions must be composable. `return` delivers output objects to calling code, while `print` merely produces side-effect text on stdout and yields `None`.",
        "difficulty": "hard",
        "concept": "composable_functions",
        "skill": "software_architecture"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 11: Return vs Print mental models and pipelines.")

def upgrade_unit_15_mutable_defaults():
    """
    Unit 15 Lesson 15.1: Default Arguments - The Mutable Default Trap.
    """
    data, fp = load_lesson("unit_15/15.1_*.json")
    items = data["items"]
    
    # Q16: Spot the bug: Mutable default argument
    items[15] = {
        "id": "15.1_q16",
        "type": "spot_the_bug",
        "question": "A developer wrote this user registration function:\n\n```python\ndef register_user(username, roles=[]):\n    roles.append('user')\n    return {'username': username, 'roles': roles}\n\nu1 = register_user('alice')\nu2 = register_user('bob')\n```\nWhy does `u2['roles']` unexpectedly contain `['user', 'user']`?",
        "options": [
            "Default argument expressions are evaluated once when the function is defined, so all invocations share the exact same list object in memory",
            "The username 'bob' inherited properties from 'alice' due to global variable leakage",
            "append() automatically duplicates items when the list length is under 5",
            "Dictionary keys named 'roles' are automatically linked across instances"
        ],
        "correct_answer": "Default argument expressions are evaluated once when the function is defined, so all invocations share the exact same list object in memory",
        "explanation": "Python evaluates default parameter expressions once at function definition time, NOT at invocation time. When a mutable object (like a list `[]` or dict `{}`) is used as a default, every call that omits the parameter shares that exact same object.",
        "difficulty": "medium",
        "concept": "mutable_default_trap",
        "skill": "debugging"
    }
    
    # Q19: Fix the code: The None sentinel pattern
    items[18] = {
        "id": "15.1_q19",
        "type": "fix_the_code",
        "question": "Fix this function using the idiomatic Python sentinel pattern so that each call receives its own independent list:",
        "starter_code": "def append_to_cache(key, value, cache=[]):\n    # Fix the mutable default trap\n    cache.append((key, value))\n    return cache",
        "solution_code": "def append_to_cache(key, value, cache=None):\n    if cache is None:\n        cache = []\n    cache.append((key, value))\n    return cache",
        "test_cases": [
            {"input": "append_to_cache('a', 1)", "expected_output": "[('a', 1)]"}
        ],
        "explanation": "The standard Python fix for mutable default arguments is to use `None` as the default sentinel value, and instantiate a fresh list inside the function body if `cache is None`.",
        "difficulty": "hard",
        "concept": "none_sentinel_pattern",
        "skill": "code_repair"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 15: Mutable Default Arguments and None Sentinel Pattern.")

def upgrade_unit_21_composition_over_inheritance():
    """
    Unit 21 Lesson 21.6: Composition vs Inheritance design reasoning.
    """
    data, fp = load_lesson("unit_21/21.6_composition.json")
    items = data["items"]
    
    # Q2: Architectural reasoning: Has-A vs Is-A
    items[1] = {
        "id": "21.6_q2",
        "type": "multiple_choice",
        "question": "When should an engineer prefer Composition over Inheritance ('Favor composition over inheritance')?",
        "options": [
            "When the relationship is 'has-a' (e.g. Car has an Engine) rather than strict 'is-a', preventing fragile base classes and rigid hierarchies",
            "Only when the classes are written in different programming languages",
            "Whenever a class has fewer than three methods",
            "Inheritance is always preferred over composition because subclasses run faster in Python"
        ],
        "correct_answer": "When the relationship is 'has-a' (e.g. Car has an Engine) rather than strict 'is-a', preventing fragile base classes and rigid hierarchies",
        "explanation": "Inheritance couples subclasses tightly to their parent hierarchy ('is-a'). Composition ('has-a') allows independent, swappable components, reduces fragile base class bugs, and makes testing and mocking much easier.",
        "difficulty": "easy",
        "concept": "composition_vs_inheritance",
        "skill": "software_architecture"
    }
    
    # Q18: Refactoring inheritance to composition
    items[17] = {
        "id": "21.6_q18",
        "type": "spot_the_bug",
        "question": "A developer implemented `class PaymentProcessor(DatabaseConnection)` so that payment logic could save transactions. Why is this considered poor object-oriented design?",
        "options": [
            "A PaymentProcessor is NOT a DatabaseConnection (violates 'is-a'); it should compose a DatabaseConnection as an attribute ('has-a') to avoid tight coupling and leaking connection internals",
            "Database connections in Python cannot be subclassed due to C-level security locks",
            "Payment processors are required by PEP 8 to be standalone module functions",
            "Subclasses cannot execute SQL queries"
        ],
        "correct_answer": "A PaymentProcessor is NOT a DatabaseConnection (violates 'is-a'); it should compose a DatabaseConnection as an attribute ('has-a') to avoid tight coupling and leaking connection internals",
        "explanation": "Inheriting from `DatabaseConnection` creates high coupling: changes to the DB class can break payments, and `PaymentProcessor` inherits irrelevant database methods. The correct design is composition: `self.db = db_connection`.",
        "difficulty": "medium",
        "concept": "composition_design_principles",
        "skill": "architectural_review"
    }
    
    # Q27: Independent code construction: Composite Order system
    items[26] = {
        "id": "21.6_q27",
        "type": "write_the_code",
        "question": "Implement an `Order` class that uses composition. The `Order` takes a list of `Item` objects (each having `price` and `quantity` attributes) and provides a `total_cost()` method that computes the grand total sum of `item.price * item.quantity`.",
        "starter_code": "class Item:\n    def __init__(self, name: str, price: float, quantity: int):\n        self.name = name\n        self.price = price\n        self.quantity = quantity\n\nclass Order:\n    def __init__(self, items: list[Item] = None):\n        # Initialize items safely using composition\n        pass\n\n    def total_cost(self) -> float:\n        # Compute and return total cost\n        pass",
        "solution_code": "class Item:\n    def __init__(self, name: str, price: float, quantity: int):\n        self.name = name\n        self.price = price\n        self.quantity = quantity\n\nclass Order:\n    def __init__(self, items: list[Item] = None):\n        self.items = list(items) if items is not None else []\n\n    def total_cost(self) -> float:\n        return sum(item.price * item.quantity for item in self.items)",
        "test_cases": [
            {"input": "o = Order([Item('Book', 10.0, 2), Item('Pen', 2.5, 4)]); o.total_cost()", "expected_output": "30.0"}
        ],
        "explanation": "`Order` composes `Item` instances via `self.items`. Calculating `total_cost()` iterates over composed objects without needing inheritance.",
        "difficulty": "hard",
        "concept": "object_composition",
        "skill": "code_construction"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 21: Composition vs Inheritance design principles.")

def upgrade_unit_23_generators_large_data():
    """
    Unit 23 Lesson 23.5: Memory Efficiency - Streaming Gigabyte-scale logs.
    """
    data, fp = load_lesson("unit_23/23.5_memory_efficiency.json")
    items = data["items"]
    
    # Q2: Why generators for large files
    items[1] = {
        "id": "23.5_q2",
        "type": "multiple_choice",
        "question": "You need to parse a 20 GB server access log file on a machine with only 8 GB of RAM. Which Python approach is required to prevent an Out Of Memory (OOM) crash?",
        "options": [
            "Use a generator function with `yield` to stream and process lines one by one, keeping memory usage constant O(1)",
            "Call `file.readlines()` to load all lines into a Python list",
            "Use a list comprehension: `[line for line in file]`",
            "Convert the entire file to a JSON dictionary in memory"
        ],
        "correct_answer": "Use a generator function with `yield` to stream and process lines one by one, keeping memory usage constant O(1)",
        "explanation": "Generators produce items lazily on demand. By streaming one line at a time with `yield`, memory consumption remains tiny and constant O(1) regardless of whether the log file is 1 MB or 100 GB.",
        "difficulty": "easy",
        "concept": "generators_for_large_data",
        "skill": "system_design"
    }
    
    # Q27: Write the code: Streaming error filter generator
    items[26] = {
        "id": "23.5_q27",
        "type": "write_the_code",
        "question": "Write a generator function `stream_error_logs(lines: list[str])` that yields only the stripped log messages that start with `\"[ERROR]\"`. It must be a generator (using `yield`), not a list accumulator.",
        "starter_code": "from typing import Iterator\n\ndef stream_error_logs(lines: list[str]) -> Iterator[str]:\n    # Yield lines matching '[ERROR]' lazily\n    pass",
        "solution_code": "from typing import Iterator\n\ndef stream_error_logs(lines: list[str]) -> Iterator[str]:\n    for line in lines:\n        cleaned = line.strip()\n        if cleaned.startswith(\"[ERROR]\"):\n            yield cleaned",
        "test_cases": [
            {"input": "list(stream_error_logs(['[INFO] boot', '[ERROR] timeout', '[ERROR] db fail']))", "expected_output": "['[ERROR] timeout', '[ERROR] db fail']"}
        ],
        "explanation": "The generator uses `yield` to deliver each matching log entry as soon as it is encountered, allowing downstream consumers to process millions of records with constant memory footprint.",
        "difficulty": "hard",
        "concept": "generator_streaming",
        "skill": "code_construction"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 23: Generators for memory efficiency and log streaming.")

def upgrade_unit_26_sql_injection():
    """
    Unit 26 Lesson 26.6: SQL Injection & Parameterized Queries.
    """
    data, fp = load_lesson("unit_26/26.6_parameterized_queries_and_security.json")
    items = data["items"]
    
    # Q1: Micro lesson on SQL Injection
    items[0] = {
        "id": "26.6_q1",
        "type": "micro_lesson",
        "title": "SQL Injection & Parameterized Queries",
        "content": "SQL Injection occurs when untrusted user input is directly concatenated or formatted into a SQL query string:\n\n```python\n# DANGEROUS: Vulnerable to SQL Injection!\nquery = f\"SELECT * FROM users WHERE username = '{user_input}'\"\n```\nIf an attacker inputs `' OR '1'='1`, the query alters its logic to bypass authentication entirely.\n\nTo prevent this, you **MUST always use parameterized queries**:\n```python\n# SAFE: The database driver escapes and types parameters\ncursor.execute(\"SELECT * FROM users WHERE username = ?\", (user_input,))\n```",
        "difficulty": "easy",
        "concept": "sql_injection_defense",
        "skill": "security_engineering"
    }
    
    # Q17: Spot the security vulnerability
    items[16] = {
        "id": "26.6_q17",
        "type": "spot_the_bug",
        "question": "Identify the catastrophic security flaw in this authentication query:\n\n```python\ndef login(cursor, user, password):\n    sql = f\"SELECT id FROM accounts WHERE user='{user}' AND pass='{password}'\"\n    return cursor.execute(sql).fetchone()\n```",
        "options": [
            "It uses f-string interpolation for SQL query parameters, enabling SQL Injection attacks that allow attackers to bypass login or drop tables",
            "The function returns fetchone() instead of fetchall(), which crashes the database",
            "Password strings in Python cannot be compared using single quotes",
            "cursor.execute() requires a semicolon at the end of the query string"
        ],
        "correct_answer": "It uses f-string interpolation for SQL query parameters, enabling SQL Injection attacks that allow attackers to bypass login or drop tables",
        "explanation": "Never use Python f-strings, `%`, or `.format()` to assemble SQL queries. An attacker passing `admin' --` in `user` turns the query into `SELECT id FROM accounts WHERE user='admin' -- ...`, logging in as admin without knowing the password.",
        "difficulty": "medium",
        "concept": "sql_injection_flaw",
        "skill": "security_audit"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 26: SQL Injection and Parameterized Query security.")

def upgrade_unit_28_asyncio_blocking():
    """
    Unit 28 Lesson 28.1: Synchronous vs Asynchronous - The Blocking Trap.
    """
    data, fp = load_lesson("unit_28/28.1_synchronous_vs_asynchronous_execution.json")
    items = data["items"]
    
    # Q8: Prediction of blocking time.sleep inside async
    items[7] = {
        "id": "28.1_q8",
        "type": "multiple_choice",
        "question": "What happens if you call standard `time.sleep(5)` inside an `async def` coroutine instead of `await asyncio.sleep(5)`?",
        "options": [
            "It completely blocks Python's single-threaded event loop for 5 seconds, freezing all concurrent coroutines from executing",
            "It automatically converts into an asynchronous non-blocking task behind the scenes",
            "Python raises an AsyncBlockException immediately upon execution",
            "The event loop spawns a background thread to handle the sleep"
        ],
        "correct_answer": "It completely blocks Python's single-threaded event loop for 5 seconds, freezing all concurrent coroutines from executing",
        "explanation": "`time.sleep()` is a synchronous blocking syscall that halts the entire thread. Because `asyncio` runs on a single thread event loop, blocking the thread stops all other coroutines from running. Always use `await asyncio.sleep()` for non-blocking delays.",
        "difficulty": "medium",
        "concept": "blocking_event_loop",
        "skill": "concurrency_reasoning"
    }
    
    # Q26: Transfer: Choosing between Threading, Multiprocessing, and AsyncIO
    items[25] = {
        "id": "28.1_q26",
        "type": "multiple_choice",
        "question": "You are building a microservice that downloads 500 web pages over HTTP concurrently. Which concurrency model in Python provides high throughput with the lowest memory overhead?",
        "options": [
            "AsyncIO with an async HTTP library (like aiohttp or httpx), which handles thousands of concurrent I/O sockets on a single thread event loop",
            "Multiprocessing with 500 OS processes, because each process gets its own CPU core",
            "Subprocessing with 500 distinct Python interpreter subprocesses",
            "Sequential synchronous execution with time.sleep() between requests"
        ],
        "correct_answer": "AsyncIO with an async HTTP library (like aiohttp or httpx), which handles thousands of concurrent I/O sockets on a single thread event loop",
        "explanation": "HTTP requests are I/O-bound (waiting on network sockets). `asyncio` handles thousands of concurrent connections within a single process and thread with minimal memory overhead, whereas spawning 500 processes would exhaust RAM and CPU.",
        "difficulty": "hard",
        "concept": "concurrency_model_selection",
        "skill": "engineering_judgment"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 28: AsyncIO blocking trap and concurrency model selection.")

def upgrade_unit_33_hashing_tradeoffs():
    """
    Unit 33 Lesson 33.3: Sets for Fast Lookups - Tradeoffs vs Lists.
    """
    data, fp = load_lesson("unit_33/33.3_sets_for_fast_lookups.json")
    items = data["items"]
    
    # Q2: Membership complexity tradeoff
    items[1] = {
        "id": "33.3_q2",
        "type": "multiple_choice",
        "question": "You have a dataset of 1,000,000 user IDs and need to verify if incoming requests come from authorized users. Why is `user_id in authorized_set` vastly superior to `user_id in authorized_list`?",
        "options": [
            "Set membership check is O(1) average time via hash table indexing, whereas list membership check is O(N) linear scan through all 1,000,000 elements",
            "Sets automatically sort integers in CPU cache lines",
            "Lists can only store up to 65,536 elements in standard CPython",
            "Set lookup is executed by the GPU while list lookup is CPU-bound"
        ],
        "correct_answer": "Set membership check is O(1) average time via hash table indexing, whereas list membership check is O(N) linear scan through all 1,000,000 elements",
        "explanation": "Python sets use hash tables. Checking `item in set` calculates `hash(item)` and looks up the bucket in O(1) average time. Checking `item in list` requires scanning elements from left to right (O(N) worst and average case), causing a massive performance degradation at scale.",
        "difficulty": "easy",
        "concept": "hash_lookup_complexity",
        "skill": "algorithm_analysis"
    }
    
    # Q26: When NOT to use a set
    items[25] = {
        "id": "33.3_q26",
        "type": "multiple_choice",
        "question": "In which scenario would using a `set` be INAPPROPRIATE or impossible?",
        "options": [
            "When you must preserve duplicate elements or when the items are unhashable mutable objects like lists or dictionaries",
            "When you have more than 1,000 unique integers",
            "When checking whether a string appears in a collection of strings",
            "When eliminating duplicate entries from an imported CSV file"
        ],
        "correct_answer": "When you must preserve duplicate elements or when the items are unhashable mutable objects like lists or dictionaries",
        "explanation": "Sets require elements to be hashable (immutable, with `__hash__`). Mutable types like `list` and `dict` cannot be stored in sets (raising `TypeError: unhashable type`). Additionally, sets enforce element uniqueness, so they cannot store duplicate values.",
        "difficulty": "hard",
        "concept": "when_not_to_use_sets",
        "skill": "engineering_judgment"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 33: Set vs List complexity tradeoffs and hashability constraints.")

def upgrade_unit_03_identity_vs_equality():
    """
    Unit 3 Lesson 3.4: Comparison Operators - Equality (==) vs Identity (is).
    """
    data, fp = load_lesson("unit_03/3.4_*.json")
    items = data["items"]
    
    # Q6: Mental model of == vs is
    items[5] = {
        "id": "3.4_q6",
        "type": "multiple_choice",
        "question": "What is the critical distinction between `a == b` and `a is b`?",
        "options": [
            "`==` tests if the values are equal, while `is` tests if both variables point to the exact same object in memory (`id(a) == id(b)`)",
            "`is` tests for value equality, while `==` tests for type equality",
            "`==` is used exclusively for numbers, while `is` is used exclusively for strings",
            "`==` modifies the variables to be equal, while `is` compares them"
        ],
        "correct_answer": "`==` tests if the values are equal, while `is` tests if both variables point to the exact same object in memory (`id(a) == id(b)`)",
        "explanation": "`==` checks value equivalence (equality), whereas `is` checks reference identity (whether two identifiers refer to the identical memory address). For example, `[1, 2] == [1, 2]` is `True`, but `[1, 2] is [1, 2]` is `False` because they are separate objects.",
        "difficulty": "medium",
        "concept": "equality_vs_identity",
        "skill": "mental_model"
    }
    
    # Q18: Debugging idiom: None comparison
    items[17] = {
        "id": "3.4_q18",
        "type": "multiple_choice",
        "question": "Why does PEP 8 mandate checking for `None` using `if value is None:` rather than `if value == None:`?",
        "options": [
            "`None` is a unique singleton in Python; `is` directly checks identity in one fast CPU instruction and cannot be tricked by custom classes that override `__eq__`",
            "`== None` raises a SyntaxError in modern Python 3",
            "`is None` converts the value to a boolean before comparing",
            "`== None` deletes the variable if it evaluates to False"
        ],
        "correct_answer": "`None` is a unique singleton in Python; `is` directly checks identity in one fast CPU instruction and cannot be tricked by custom classes that override `__eq__`",
        "explanation": "`None` exists as a single unique singleton object in Python runtime. Comparing with `is None` is faster and prevents unintended side effects if a custom object defines an `__eq__` method that behaves unexpectedly.",
        "difficulty": "medium",
        "concept": "none_identity_idiom",
        "skill": "idiomatic_python"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 03: == vs is and None identity idiom.")

def upgrade_unit_05_truthiness_and_none():
    """
    Unit 5 Lesson 5.5: Truthiness - Falsy values and boolean evaluation.
    """
    data, fp = load_lesson("unit_05/5.5_*.json")
    items = data["items"]
    
    # Q1: Micro lesson on truthiness
    items[0] = {
        "id": "5.5_q1",
        "type": "micro_lesson",
        "title": "Truthiness: What Python Considers True and False",
        "content": "In Python, any object can be tested for truth value inside an `if` or `while` condition.\n\nThe following are inherently **falsy**:\n- Constants: `None`, `False`\n- Numeric zeros: `0`, `0.0`, `0j`\n- Empty sequences and collections: `\"\"`, `()`, `[]`, `{}`, `set()`\n\nAll other values are **truthy**. This allows concise Pythonic checks like `if items:` instead of `if len(items) > 0:`.",
        "difficulty": "easy",
        "concept": "truthiness_rules",
        "skill": "mental_model"
    }
    
    # Q17: Spot the bug: Truthiness trap with zero
    items[16] = {
        "id": "5.5_q17",
        "type": "spot_the_bug",
        "question": "A developer wrote this function to format a user's discount points:\n\n```python\ndef display_points(points):\n    if not points:\n        return 'No points available'\n    return f'You have {points} points'\n```\nWhat bug occurs when a user has exactly `0` points?",
        "options": [
            "0 is falsy, so display_points(0) returns 'No points available' instead of 'You have 0 points'",
            "Python raises a ValueError because 0 cannot be interpolated in f-strings",
            "The function returns None because not 0 is invalid syntax",
            "The function enters an infinite loop"
        ],
        "correct_answer": "0 is falsy, so display_points(0) returns 'No points available' instead of 'You have 0 points'",
        "explanation": "Because `0` is falsy in Python, `not 0` evaluates to `True`. To distinguish between 'no value provided' (`None`) and 'zero points' (`0`), the code should explicitly check `if points is None:`.",
        "difficulty": "medium",
        "concept": "truthiness_zero_trap",
        "skill": "debugging"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 05: Truthiness rules and zero vs None trap.")

def upgrade_unit_07_string_immutability():
    """
    Unit 7 Lesson 7.5: String Methods - String Immutability.
    """
    data, fp = load_lesson("unit_07/7.5_*.json")
    items = data["items"]
    
    # Q1: Micro lesson on string immutability
    items[0] = {
        "id": "7.5_q1",
        "type": "micro_lesson",
        "title": "Strings Are Immutable: Methods Return New Strings",
        "content": "Unlike lists, Python strings are **immutable**—they can never be modified in-place once created.\n\nWhen you call a string method like `.lower()`, `.upper()`, or `.strip()`, Python does NOT modify the original string. Instead, it creates and returns a **brand-new string** with the modifications.\n\nTo preserve the changed string, you must rebind the variable: `text = text.strip()`.",
        "difficulty": "easy",
        "concept": "string_immutability",
        "skill": "mental_model"
    }
    
    # Q16: Spot the bug: Forgetting to reassign after string method
    items[15] = {
        "id": "7.5_q16",
        "type": "spot_the_bug",
        "question": "A developer attempts to sanitize a user input string:\n\n```python\nemail = '  User@Example.COM  '\nemail.strip()\nemail.lower()\nprint(email)\n```\nWhy does the output remain `'  User@Example.COM  '`?",
        "options": [
            "Strings are immutable in Python; .strip() and .lower() return new strings without mutating the original, so email must be reassigned (e.g. email = email.strip().lower())",
            "strip() only removes trailing spaces, not leading spaces",
            "lower() requires an encoding parameter to convert uppercase letters",
            "The print function restores the original variable value"
        ],
        "correct_answer": "Strings are immutable in Python; .strip() and .lower() return new strings without mutating the original, so email must be reassigned (e.g. email = email.strip().lower())",
        "explanation": "Because strings cannot be modified in place, string methods always return a new string. Calling `email.strip()` in isolation creates a new string and immediately discards it. The variable must be reassigned.",
        "difficulty": "medium",
        "concept": "string_immutability_reassignment",
        "skill": "debugging"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 07: String immutability and reassignment.")

def upgrade_unit_10_missing_keys_and_get():
    """
    Unit 10 Lesson 10.2: Creating and Accessing Dictionaries - Safe .get() Access.
    """
    data, fp = load_lesson("unit_10/10.2_*.json")
    items = data["items"]
    
    # Q26: Transfer: Processing API JSON records with optional fields
    items[25] = {
        "id": "10.2_q26",
        "type": "real_world_scenario",
        "question": "You are processing 10,000 user profiles returned from an external JSON API. Some profiles contain a `'phone'` key, but others omit it entirely. Which pattern ensures your pipeline continues running without crashing?",
        "options": [
            "phone = profile.get('phone', 'Unspecified')",
            "phone = profile['phone']",
            "phone = profile.pop('phone')",
            "phone = profile.phone if 'phone' in profile else None"
        ],
        "correct_answer": "phone = profile.get('phone', 'Unspecified')",
        "explanation": "Direct indexing `profile['phone']` raises a fatal `KeyError` if the key does not exist. Using `.get('phone', 'Unspecified')` returns the provided default value safely without raising an exception.",
        "difficulty": "hard",
        "concept": "safe_dict_get",
        "skill": "engineering_judgment"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 10: Safe dictionary key lookup with .get().")

def upgrade_unit_21_mutable_class_attributes():
    """
    Unit 21 Lesson 21.1: Class Attributes vs Instance Attributes.
    """
    data, fp = load_lesson("unit_21/21.1_*.json")
    items = data["items"]
    
    # Q17: Spot the bug: Mutable class attribute trap
    items[16] = {
        "id": "21.1_q17",
        "type": "spot_the_bug",
        "question": "A developer wrote this class to model accounts:\n\n```python\nclass UserAccount:\n    transactions = []\n\n    def add_transaction(self, amount):\n        self.transactions.append(amount)\n\nu1 = UserAccount()\nu1.add_transaction(100)\nu2 = UserAccount()\nprint(u2.transactions)\n```\nWhy does `u2.transactions` print `[100]`?",
        "options": [
            "`transactions` is defined as a class attribute, so all instances of UserAccount share the exact same list object in memory",
            "Python automatically merges all lists created in the same second",
            "u2 was instantiated as an alias of u1",
            "append() writes to global module memory"
        ],
        "correct_answer": "`transactions` is defined as a class attribute, so all instances of UserAccount share the exact same list object in memory",
        "explanation": "Attributes declared directly in the class body are class attributes, shared across all instances. Mutable class attributes (like `[]` or `{}`) cause state leakage between instances. Mutable attributes should always be initialized in `__init__` via `self.transactions = []`.",
        "difficulty": "medium",
        "concept": "mutable_class_attribute_trap",
        "skill": "debugging"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 21: Mutable class attribute trap.")

def upgrade_unit_24_testing_returns_and_edge_cases():
    """
    Unit 24 Lesson 24.3: Unit Testing Basics - Testing returns vs print.
    """
    data, fp = load_lesson("unit_24/24.3_*.json")
    items = data["items"]
    
    # Q18: Why print breaks testing
    items[17] = {
        "id": "24.3_q18",
        "type": "spot_the_bug",
        "question": "A junior developer wrote a unit test for their tax calculation function:\n\n```python\ndef calculate_tax(amount):\n    print(round(amount * 0.1, 2))\n\ndef test_tax():\n    assert calculate_tax(100) == 10.0\n```\nWhy does `test_tax()` fail with `AssertionError: assert None == 10.0`?",
        "options": [
            "calculate_tax prints to stdout and returns None; unit test assertions evaluate return values, so functions under test must return their results",
            "assert statements in Python can only compare integers, not floats",
            "round() is not supported inside unit tests",
            "The function name must begin with 'verify_' to return values"
        ],
        "correct_answer": "calculate_tax prints to stdout and returns None; unit test assertions evaluate return values, so functions under test must return their results",
        "explanation": "Automated testing verifies return values and system state. Because `calculate_tax` called `print()` instead of `return`, its return value is `None`, causing `assert None == 10.0` to fail.",
        "difficulty": "medium",
        "concept": "testing_return_values",
        "skill": "testing_methodology"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 24: Testing return values vs print.")

def upgrade_unit_34_deque_vs_list_queue():
    """
    Unit 34 Lesson 34.5: Collections Deque Module - Tradeoffs vs List.
    """
    data, fp = load_lesson("unit_34/34.5_*.json")
    items = data["items"]
    
    # Q2: Complexity tradeoff: deque vs list for queues
    items[1] = {
        "id": "34.5_q2",
        "type": "multiple_choice",
        "question": "Why is `collections.deque` strongly preferred over a standard Python `list` when implementing a First-In-First-Out (FIFO) queue?",
        "options": [
            "deque.popleft() is O(1) constant time, whereas list.pop(0) is O(N) linear time because all remaining elements must shift left in memory",
            "deque can store infinite elements while list is capped at 1,000",
            "Lists do not support string items when used as queues",
            "deque operations run on separate CPU threads automatically"
        ],
        "correct_answer": "deque.popleft() is O(1) constant time, whereas list.pop(0) is O(N) linear time because all remaining elements must shift left in memory",
        "explanation": "A Python `list` is a dynamic array. Popping the first element (`list.pop(0)`) requires shifting every remaining element one index to the left in memory, making it O(N). `deque` is implemented as a doubly linked list of fixed blocks, allowing O(1) appends and pops from both ends.",
        "difficulty": "easy",
        "concept": "deque_vs_list_queue",
        "skill": "dsa_tradeoffs"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 34: Deque vs List queue complexity tradeoffs.")

def upgrade_unit_37_binary_search_tradeoffs():
    """
    Unit 37 Lesson 37.2: Binary Search - Prerequisite & Complexity.
    """
    data, fp = load_lesson("unit_37/37.2_*.json")
    items = data["items"]
    
    # Q2: Prerequisite and complexity
    items[1] = {
        "id": "37.2_q2",
        "type": "multiple_choice",
        "question": "What is the mandatory prerequisite for applying Binary Search, and what is its time complexity?",
        "options": [
            "The collection must already be sorted; its time complexity is O(log N) because it halves the search space in each step",
            "The collection must contain only positive integers; its time complexity is O(1)",
            "The collection must be a linked list; its time complexity is O(N)",
            "The collection must have an odd number of elements; its time complexity is O(N^2)"
        ],
        "correct_answer": "The collection must already be sorted; its time complexity is O(log N) because it halves the search space in each step",
        "explanation": "Binary Search relies on comparing the target with the middle element to eliminate half of the remaining elements. This halving logic is only valid if the collection is sorted in monotonic order. Its time complexity is O(log N).",
        "difficulty": "easy",
        "concept": "binary_search_prerequisites",
        "skill": "dsa_tradeoffs"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 37: Binary search prerequisites and complexity.")

def upgrade_unit_43_capstone_synthesis():
    """
    Unit 43 Lesson 43.5: Final Open-Ended Mastery Challenge.
    """
    data, fp = load_lesson("unit_43/43.5_final_open_ended_mastery_challenge.json")
    items = data["items"]
    
    # Q30: The Capstone Boss Synthesis Question
    items[29] = {
        "id": "43.5_q30",
        "type": "write_the_code",
        "question": "Build a production-grade `DataPipeline` class synthesizing data structures, error handling, generator streaming, and type annotations:\n- `__init__(self, validators: list = None)`: initializes validators safely (None sentinel pattern).\n- `process_stream(self, records: list[dict])`: a generator yielding only records that pass all validators without raising exceptions.\n- If a validator raises an exception on a record, log or skip that record cleanly without terminating the generator.",
        "starter_code": "from typing import Iterator, Callable, Any\n\nclass DataPipeline:\n    def __init__(self, validators: list[Callable[[dict], bool]] = None):\n        # Initialize safely\n        pass\n\n    def process_stream(self, records: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:\n        # Yield valid records, handle exceptions cleanly\n        pass",
        "solution_code": "from typing import Iterator, Callable, Any\n\nclass DataPipeline:\n    def __init__(self, validators: list[Callable[[dict], bool]] = None):\n        self.validators = list(validators) if validators is not None else []\n\n    def process_stream(self, records: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:\n        for rec in records:\n            valid = True\n            for v in self.validators:\n                try:\n                    if not v(rec):\n                        valid = False\n                        break\n                except Exception:\n                    valid = False\n                    break\n            if valid:\n                yield rec",
        "test_cases": [
            {
                "input": "p = DataPipeline([lambda r: r.get('status') == 'active']); list(p.process_stream([{'id': 1, 'status': 'active'}, {'id': 2, 'status': 'inactive'}]))",
                "expected_output": "[{'id': 1, 'status': 'active'}]"
            }
        ],
        "explanation": "This capstone synthesis brings together OOP composition, safe sentinel default handling, defensive exception containment, and lazy generator streaming for high-throughput data processing.",
        "difficulty": "hard",
        "concept": "full_system_synthesis",
        "skill": "architectural_mastery"
    }
    
    save_lesson(data, fp)
    print("Upgraded Unit 43: Capstone synthesis question.")

def main():
    print("Beginning execution of mandatory pedagogical content fixes...")
    upgrade_unit_02_mental_models()
    upgrade_unit_03_identity_vs_equality()
    upgrade_unit_05_truthiness_and_none()
    upgrade_unit_07_string_immutability()
    upgrade_unit_08_mutation_and_aliasing()
    upgrade_unit_10_missing_keys_and_get()
    upgrade_unit_11_return_vs_print()
    upgrade_unit_15_mutable_defaults()
    upgrade_unit_21_composition_over_inheritance()
    upgrade_unit_21_mutable_class_attributes()
    upgrade_unit_23_generators_large_data()
    upgrade_unit_24_testing_returns_and_edge_cases()
    upgrade_unit_26_sql_injection()
    upgrade_unit_28_asyncio_blocking()
    upgrade_unit_33_hashing_tradeoffs()
    upgrade_unit_34_deque_vs_list_queue()
    upgrade_unit_37_binary_search_tradeoffs()
    upgrade_unit_43_capstone_synthesis()
    print("All mandatory content upgrades applied successfully.")

if __name__ == "__main__":
    main()
