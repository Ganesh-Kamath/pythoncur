"""
CODOLINGO EXACT REPAIRS: TESTING (30.6) AND FINAL MASTERY (43.5)
Defines authentic pedagogical replacements for:
- 30.6 (q1, q3, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q22)
- 43.5 (q13, q14, q15, q16, q17, q18)
"""

REPLACEMENTS_MASTERY_AND_TESTING = {
    # ==========================================
    # UNIT 30.6: TESTING A SOLUTION
    # ==========================================
    "30.6_q1": {
        "id": "30.6_q1",
        "type": "micro_lesson",
        "concept": "testing_a_solution_methodology",
        "skill": "test_design",
        "difficulty": "medium",
        "prerequisites": [],
        "prompt": "# Systematic Solution Testing Methodology\n\nTesting is not merely running code once with the example input. A professional testing workflow follows four rigorous stages:\n\n1. **Happy Path:** Verify standard valid inputs with known answers.\n2. **Boundary Values:** Test extrema (e.g. empty lists `[]`, zero `0`, negative numbers, 1-element collections).\n3. **Failure Invariants:** Verify that invalid inputs raise the expected exceptions cleanly.\n4. **Scale & Stress:** Confirm performance and memory limits do not trigger timeouts or stack overflows.",
        "explanation": "Mastering systematic test categorization ensures no silent edge-case regressions reach production.",
        "metadata": {
            "concept": "systematic_test_methodology",
            "skill": "testing",
            "learning_objective": "Structure tests across happy path, boundaries, invariants, and scale",
            "why_this_exercise_exists": "Replaces generic placeholder with real testing methodology"
        }
    },
    "30.6_q3": {
        "id": "30.6_q3",
        "type": "micro_lesson",
        "concept": "testing_a_solution_triangulation",
        "skill": "test_triangulation",
        "difficulty": "medium",
        "prerequisites": ["30.6_q2"],
        "prompt": "# Test Triangulation and Defect Localization\n\nWhen a test fails, do not guess at the fix:\n\n1. **Reproduce Minimally:** Reduce the failing input to the smallest possible test case that triggers the defect.\n2. **Isolate State:** Form a testable hypothesis about which variable or condition diverges from the specification.\n3. **Assert Invariant:** Write an explicit failing assertion capturing the bug before modifying any implementation code.",
        "explanation": "Writing an assertion that reproduces the bug before fixing it ensures proof of defect and prevents regression.",
        "metadata": {
            "concept": "defect_localization",
            "skill": "debugging_methodology",
            "learning_objective": "Formulate minimal reproducible test cases to isolate defects",
            "why_this_exercise_exists": "Replaces generic placeholder with industry debugging standard"
        }
    },
    "30.6_q7": {
        "id": "30.6_q7",
        "type": "error_diagnosis",
        "concept": "testing_a_solution_bug_hunt_1",
        "skill": "bug_hunting",
        "difficulty": "medium",
        "prerequisites": ["30.6_q6"],
        "prompt": "Discover the bug in this function by inspecting the test case:\n\n```python\ndef binary_search(arr, target):\n    low = 0\n    high = len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid  # Bug here!\n        else:\n            high = mid - 1\n    return -1\n```\n\nWhat happens when testing with `arr = [1, 3, 5]` and `target = 5`?",
        "options": [
            "Infinite loop! When low=1 and high=2, mid evaluates to 1 and setting low = mid leaves low at 1 forever.",
            "IndexError: list index out of range.",
            "Returns -1 incorrectly.",
            "Raises a TypeError."
        ],
        "correct_answer": "Infinite loop! When low=1 and high=2, mid evaluates to 1 and setting low = mid leaves low at 1 forever.",
        "explanation": "Because `mid` can equal `low` during integer division `(low + high) // 2`, assigning `low = mid` fails to advance the search window, causing an infinite loop. The fix is `low = mid + 1`.",
        "metadata": {
            "concept": "binary_search_infinite_loop_bug",
            "skill": "bug_hunting",
            "learning_objective": "Discover off-by-one infinite loops in binary search through boundary tests",
            "common_misconception": "Thinking low = mid advances the search range",
            "why_this_exercise_exists": "Teaches bug discovery through concrete test tracing"
        }
    },
    "30.6_q8": {
        "id": "30.6_q8",
        "type": "output_prediction",
        "concept": "testing_a_solution_boundary_test",
        "skill": "boundary_testing",
        "difficulty": "medium",
        "prerequisites": ["30.6_q7"],
        "prompt": "Which test case exposes the flaw in this naive palindrome checker?\n\n```python\ndef is_palindrome(text):\n    return text == text[::-1]\n```",
        "options": [
            "is_palindrome('Racecar') returning False because case sensitivity is not handled.",
            "is_palindrome('radar') returning True.",
            "is_palindrome('') returning True.",
            "is_palindrome('a') returning True."
        ],
        "correct_answer": "is_palindrome('Racecar') returning False because case sensitivity is not handled.",
        "explanation": "'Racecar' is a valid palindrome in natural language, but `'Racecar'[::-1]` is `'racecaR'`. Without normalizing case via `.lower()`, case mismatch causes the test to fail.",
        "metadata": {
            "concept": "case_insensitivity_boundary",
            "skill": "test_case_design",
            "learning_objective": "Design test cases revealing unhandled string normalization requirements",
            "common_misconception": "Testing only all-lowercase words",
            "why_this_exercise_exists": "Highlights real-world input variance in test design"
        }
    },
    "30.6_q9": {
        "id": "30.6_q9",
        "type": "code_prediction",
        "concept": "testing_a_solution_empty_collection",
        "skill": "edge_case_testing",
        "difficulty": "medium",
        "prerequisites": ["30.6_q8"],
        "prompt": "What happens when testing `find_max(numbers)` with an empty list `[]`?\n\n```python\ndef find_max(numbers):\n    highest = numbers[0]\n    for n in numbers:\n        if n > highest:\n            highest = n\n    return highest\n```",
        "options": [
            "Raises IndexError: list index out of range on numbers[0].",
            "Returns None cleanly.",
            "Returns 0.",
            "Returns -1."
        ],
        "correct_answer": "Raises IndexError: list index out of range on numbers[0].",
        "explanation": "Accessing `numbers[0]` when `numbers` is empty immediately crashes with an `IndexError`. Robust functions must check `if not numbers:` and raise a descriptive error or return a designated default (such as `None`).",
        "metadata": {
            "concept": "empty_collection_index_error",
            "skill": "edge_case_testing",
            "learning_objective": "Test functions against empty inputs to catch unguarded indexing errors",
            "common_misconception": "Assuming input lists are never empty",
            "why_this_exercise_exists": "Catches unguarded indexing bugs before production"
        }
    },
    "30.6_q10": {
        "id": "30.6_q10",
        "type": "write_the_code",
        "concept": "testing_a_solution_test_suite_authoring",
        "skill": "test_suite_design",
        "difficulty": "medium",
        "prerequisites": ["30.6_q9"],
        "prompt": "Write a unit test function `test_divide()` with assertions that test:\n1. Normal division: `divide(10, 2) == 5.0`\n2. Negative division: `divide(-9, 3) == -3.0`\n3. Division by zero: raises `ZeroDivisionError` using a `try/except` block.",
        "starter_code": "def divide(a, b):\n    return a / b\n\ndef test_divide():\n    # Write comprehensive test suite\n    pass",
        "solution_code": "def divide(a, b):\n    return a / b\n\ndef test_divide():\n    assert divide(10, 2) == 5.0, \"Should divide positive numbers\"\n    assert divide(-9, 3) == -3.0, \"Should handle negative numbers\"\n    \n    caught = False\n    try:\n        divide(10, 0)\n    except ZeroDivisionError:\n        caught = True\n    assert caught, \"Should raise ZeroDivisionError when denominator is zero\"\n\ntest_divide()\nprint(\"All division tests passed\")",
        "explanation": "A complete test suite tests both standard operation and exceptional conditions, verifying error boundaries.",
        "metadata": {
            "concept": "exception_testing_assertions",
            "skill": "test_authoring",
            "learning_objective": "Write automated assertion tests covering both happy path and exceptions",
            "common_misconception": "Omitting exception path testing",
            "why_this_exercise_exists": "Teaches thorough test harness creation"
        }
    },
    "30.6_q11": {
        "id": "30.6_q11",
        "type": "write_the_code",
        "concept": "testing_a_solution_floating_point_precision",
        "skill": "precision_testing",
        "difficulty": "medium",
        "prerequisites": ["30.6_q10"],
        "prompt": "Why does `assert 0.1 + 0.2 == 0.3` fail in Python, and how do you write the correct test using `math.isclose`?",
        "starter_code": "import math\n# Fix the floating point equality assertion\n",
        "solution_code": "import math\n# 0.1 + 0.2 evaluates to 0.30000000000000004 due to IEEE 754 float representation\nassert math.isclose(0.1 + 0.2, 0.3), \"Float arithmetic should be tested with math.isclose\"",
        "explanation": "Floating-point numbers cannot represent some decimal fractions exactly in binary IEEE-754. Exact equality `==` fails; testing must use `math.isclose(a, b)` with a small tolerance.",
        "metadata": {
            "concept": "float_equality_isclose",
            "skill": "testing_best_practices",
            "learning_objective": "Test floating-point calculations safely using math.isclose()",
            "common_misconception": "Using == for float assertions",
            "why_this_exercise_exists": "Saves developers from flaky float equality test failures"
        }
    },
    "30.6_q12": {
        "id": "30.6_q12",
        "type": "output_prediction",
        "concept": "testing_a_solution_side_effects",
        "skill": "side_effect_testing",
        "difficulty": "medium",
        "prerequisites": ["30.6_q11"],
        "prompt": "What unintended side effect does this test expose?\n\n```python\ndef append_total(items):\n    items.append(sum(items))\n    return items\n\noriginal = [1, 2, 3]\nres = append_total(original)\nprint(original)\n```",
        "options": [
            "[1, 2, 3, 6] (The function mutated the caller's original list in place!).",
            "[1, 2, 3] (original was unaffected).",
            "[6].",
            "TypeError."
        ],
        "correct_answer": "[1, 2, 3, 6] (The function mutated the caller's original list in place!).",
        "explanation": "In Python, passing a mutable object like a `list` allows the function to mutate it in place. Testing must verify not only the return value, but also that caller inputs are not unexpectedly modified.",
        "metadata": {
            "concept": "side_effect_invariant_testing",
            "skill": "testing",
            "learning_objective": "Test for unintended mutable object side-effects in functions",
            "common_misconception": "Assuming functions receive copies of lists",
            "why_this_exercise_exists": "Catches subtle data corruption side effects"
        }
    },
    "30.6_q13": {
        "id": "30.6_q13",
        "type": "fill_in_the_blank",
        "concept": "testing_a_solution_assert_syntax",
        "skill": "syntax",
        "difficulty": "medium",
        "prerequisites": ["30.6_q12"],
        "prompt": "Fill in the blank to assert that `result` equals `expected` with an optional error message:\n\n```python\n___ result == expected, f'Expected {expected} but received {result}'\n```",
        "correct_answer": "assert",
        "accepted_answers": ["assert"],
        "explanation": "The `assert` keyword evaluates a condition. If the condition evaluates to `False`, Python raises an `AssertionError` displaying the provided message.",
        "metadata": {
            "concept": "assert_statement",
            "skill": "syntax",
            "learning_objective": "Use the assert statement with informative failure messages",
            "why_this_exercise_exists": "Standard Python testing assertion keyword"
        }
    },
    "30.6_q14": {
        "id": "30.6_q14",
        "type": "multiple_choice",
        "concept": "testing_a_solution_regression_testing",
        "skill": "methodology",
        "difficulty": "medium",
        "prerequisites": ["30.6_q13"],
        "prompt": "What is a 'Regression Test' in software development?",
        "options": [
            "A test written specifically to ensure that a previously fixed bug does not reappear in future updates.",
            "A test that measures CPU clock regression.",
            "A test run only on deprecated versions of Python.",
            "A test that converts code back into pseudo-code."
        ],
        "correct_answer": "A test written specifically to ensure that a previously fixed bug does not reappear in future updates.",
        "explanation": "When a bug is fixed, a regression test is added to the automated test suite so that any future changes that accidentally reintroduce the defect will be immediately caught.",
        "metadata": {
            "concept": "regression_testing",
            "skill": "software_lifecycle",
            "learning_objective": "Understand the role and importance of regression testing",
            "common_misconception": "Discarding test cases once the bug fix passes",
            "why_this_exercise_exists": "Industry software engineering methodology"
        }
    },
    "30.6_q15": {
        "id": "30.6_q15",
        "type": "code_ordering",
        "concept": "testing_a_solution_tdd_cycle",
        "skill": "test_driven_development",
        "difficulty": "medium",
        "prerequisites": ["30.6_q14"],
        "prompt": "Order the steps of the classic Test-Driven Development (TDD) 'Red-Green-Refactor' cycle:",
        "options": [
            "Write a failing automated test specifying desired behavior",
            "Run the test and observe it fail (Red)",
            "Write minimal code required to make the test pass (Green)",
            "Refactor code for cleanliness and design while keeping tests green"
        ],
        "correct_answer": [
            "Write a failing automated test specifying desired behavior",
            "Run the test and observe it fail (Red)",
            "Write minimal code required to make the test pass (Green)",
            "Refactor code for cleanliness and design while keeping tests green"
        ],
        "explanation": "TDD follows Red (write failing test), Green (make it pass), Refactor (improve structure with test safety net).",
        "metadata": {
            "concept": "tdd_cycle",
            "skill": "methodology",
            "learning_objective": "Sequence the steps of the Test-Driven Development cycle",
            "why_this_exercise_exists": "Core developer methodology"
        }
    },
    "30.6_q16": {
        "id": "30.6_q16",
        "type": "code_prediction",
        "concept": "testing_a_solution_mocking",
        "skill": "isolation",
        "difficulty": "medium",
        "prerequisites": ["30.6_q15"],
        "prompt": "Why do unit tests use test doubles (mocks) for external network requests or database connections?",
        "options": [
            "To make tests deterministic, fast, and repeatable without requiring real network or database infrastructure.",
            "Because Python cannot connect to databases during tests.",
            "To bypass Python's security manager.",
            "Mocks increase bandwidth speed."
        ],
        "correct_answer": "To make tests deterministic, fast, and repeatable without requiring real network or database infrastructure.",
        "explanation": "External APIs may experience downtime, rate limiting, or network delays. Mocking isolates the system-under-test so unit tests run in milliseconds without external dependencies.",
        "metadata": {
            "concept": "mocking_and_isolation",
            "skill": "architecture",
            "learning_objective": "Recognize the purpose of mocking external dependencies in unit testing",
            "common_misconception": "Running unit tests against live third-party production servers",
            "why_this_exercise_exists": "Essential for reliable CI/CD pipelines"
        }
    },
    "30.6_q17": {
        "id": "30.6_q17",
        "type": "multiple_choice",
        "concept": "testing_a_solution_code_coverage",
        "skill": "metrics",
        "difficulty": "medium",
        "prerequisites": ["30.6_q16"],
        "prompt": "Does 100% line code coverage guarantee that software is free of bugs?",
        "options": [
            "No; 100% coverage only means every line was executed at least once, but does not guarantee all input combinations, edge cases, or logic boundary states were tested.",
            "Yes; 100% coverage mathematically proves code correctness.",
            "Yes; compiler errors cannot exist if coverage is 100%.",
            "No; coverage only applies to docstrings."
        ],
        "correct_answer": "No; 100% coverage only means every line was executed at least once, but does not guarantee all input combinations, edge cases, or logic boundary states were tested.",
        "explanation": "Coverage tools measure execution paths, not logic validity. A test can execute every line of a division function without ever testing the denominator `0` boundary.",
        "metadata": {
            "concept": "code_coverage_limitations",
            "skill": "testing_philosophy",
            "learning_objective": "Understand that high coverage does not equate to defect-free software",
            "common_misconception": "Equating 100% code coverage with 100% bug-free software",
            "why_this_exercise_exists": "Critical professional perspective on testing metrics"
        }
    },
    "30.6_q18": {
        "id": "30.6_q18",
        "type": "fill_in_the_blank",
        "concept": "testing_a_solution_pytest_convention",
        "skill": "tooling",
        "difficulty": "medium",
        "prerequisites": ["30.6_q17"],
        "prompt": "By standard convention, test files and test functions in pytest must start with the prefix `___` (e.g. `___calculator.py` and `def ___add():`).",
        "correct_answer": "test_",
        "accepted_answers": ["test_", "test"],
        "explanation": "Pytest automatically discovers and runs tests matching the naming convention `test_*.py` and `def test_*():`.",
        "metadata": {
            "concept": "pytest_discovery_conventions",
            "skill": "tooling",
            "learning_objective": "Adopt standard test discovery naming conventions",
            "why_this_exercise_exists": "Standard ecosystem discovery rule"
        }
    },
    "30.6_q19": {
        "id": "30.6_q19",
        "type": "fix_the_code",
        "concept": "testing_a_solution_bug_hunt_2",
        "skill": "bug_hunting",
        "difficulty": "medium",
        "prerequisites": ["30.6_q18"],
        "prompt": "A discount function fails its boundary test: `apply_discount(100, 0.1)` should return `90.0`, but currently returns `10.0` because it returns the discount amount rather than the final price! Fix the function.\n\n```python\ndef apply_discount(price, rate):\n    # Fix return value:\n    return price * rate\n```",
        "starter_code": "def apply_discount(price, rate):\n    return price * rate",
        "solution_code": "def apply_discount(price, rate):\n    return price * (1 - rate)",
        "explanation": "Returning `price * rate` returns the discount itself. Subtracting it from the original price (`price * (1 - rate)`) gives the correct discounted price.",
        "metadata": {
            "concept": "business_logic_test_failure",
            "skill": "repair",
            "learning_objective": "Diagnose and fix calculation bugs uncovered by unit test assertions",
            "common_misconception": "Returning delta instead of new absolute state",
            "why_this_exercise_exists": "Directly models finding and repairing a logic bug through test output"
        }
    },
    "30.6_q22": {
        "id": "30.6_q22",
        "type": "fix_the_code",
        "concept": "testing_a_solution_bug_hunt_3",
        "skill": "bug_hunting",
        "difficulty": "medium",
        "prerequisites": ["30.6_q21"],
        "prompt": "Testing `is_all_positive([-1, 0, 5])` fails because `0` is mistakenly treated as positive. Fix the comparison so only strictly positive numbers (`> 0`) return True.\n\n```python\ndef is_all_positive(numbers):\n    # Fix condition:\n    return all(n >= 0 for n in numbers)\n```",
        "starter_code": "def is_all_positive(numbers):\n    return all(n >= 0 for n in numbers)",
        "solution_code": "def is_all_positive(numbers):\n    return all(n > 0 for n in numbers)",
        "explanation": "Zero is neither positive nor negative. A boundary test passing `0` catches the flaw in `>= 0`. Changing to `n > 0` ensures strictly positive validation.",
        "metadata": {
            "concept": "zero_boundary_testing",
            "skill": "repair",
            "learning_objective": "Fix zero-boundary comparison bugs revealed by test cases",
            "common_misconception": "Treating 0 as a positive number in arithmetic filters",
            "why_this_exercise_exists": "Classic boundary condition discovered through testing"
        }
    },

    # ==========================================
    # UNIT 43.5: FINAL MASTERY CHALLENGE
    # ==========================================
    "43.5_q13": {
        "id": "43.5_q13",
        "type": "code_prediction",
        "concept": "final_mastery_multi_paradigm_pipeline",
        "skill": "composite_analysis",
        "difficulty": "hard",
        "prerequisites": ["43.5_q12"],
        "prompt": "Trace this composite data processing pipeline that merges dictionaries, handles exceptions, and applies comprehensions:\n\n```python\nraw_data = [\n    {\"sku\": \"A1\", \"price\": \"19.99\", \"stock\": 5},\n    {\"sku\": \"B2\", \"price\": \"invalid\", \"stock\": 0},\n    {\"sku\": \"C3\", \"price\": \"45.00\", \"stock\": 2}\n]\n\ndef parse_inventory(records):\n    inventory = {}\n    for r in records:\n        try:\n            p = float(r[\"price\"])\n            if r[\"stock\"] > 0:\n                inventory[r[\"sku\"]] = round(p * r[\"stock\"], 2)\n        except (ValueError, KeyError):\n            continue\n    return inventory\n\nval = parse_inventory(raw_data)\nprint(val)\n```\n\nWhat is output?",
        "options": [
            "{'A1': 99.95, 'C3': 90.0}",
            "{'A1': 99.95, 'B2': 0, 'C3': 90.0}",
            "{'A1': 19.99, 'C3': 45.00}",
            "ValueError"
        ],
        "correct_answer": "{'A1': 99.95, 'C3': 90.0}",
        "explanation": "`A1` is parsed and multiplied: `19.99 * 5 = 99.95`. `B2` has an invalid price which raises `ValueError` caught by the `except` block and skipped. `C3` evaluates to `45.00 * 2 = 90.0`.",
        "metadata": {
            "concept": "composite_data_pipeline_tracing",
            "skill": "system_tracing",
            "learning_objective": "Trace realistic data processing combining exceptions, dictionaries, and numeric casting",
            "common_misconception": "Thinking invalid entries crash the entire pipeline",
            "why_this_exercise_exists": "Replaces trivial string assignment with real multi-concept mastery"
        }
    },
    "43.5_q14": {
        "id": "43.5_q14",
        "type": "error_diagnosis",
        "concept": "final_mastery_concurrency_race_condition",
        "skill": "concurrency",
        "difficulty": "expert",
        "prerequisites": ["43.5_q13"],
        "prompt": "In a multithreaded Python application, why can two threads concurrently running `balance += 100` cause lost updates even though Python has a Global Interpreter Lock (GIL)?",
        "options": [
            "balance += 100 bytecode consists of multiple operations (LOAD, ADD, STORE); thread switching between them causes race conditions.",
            "The GIL prevents threads from running simultaneously on multicore CPUs entirely.",
            "Integers are mutable objects that can be corrupted in memory.",
            "Python does not support threading."
        ],
        "correct_answer": "balance += 100 bytecode consists of multiple operations (LOAD, ADD, STORE); thread switching between them causes race conditions.",
        "explanation": "`balance += 100` is NOT an atomic operation. Under the hood, Python compiles it into multiple bytecode instructions: `LOAD_NAME`, `LOAD_CONST`, `BINARY_OP`, `STORE_NAME`. A thread switch can happen between the read and write, causing race conditions unless protected by a `threading.Lock`.",
        "metadata": {
            "concept": "gil_and_bytecode_atomicity",
            "skill": "concurrency_mastery",
            "learning_objective": "Understand that the GIL does not eliminate thread race conditions",
            "common_misconception": "Believing the GIL makes all Python code thread-safe without locks",
            "why_this_exercise_exists": "Replaces basic comparison with deep multi-threading mastery"
        }
    },
    "43.5_q15": {
        "id": "43.5_q15",
        "type": "refactoring_challenge",
        "concept": "final_mastery_generator_streaming",
        "skill": "memory_architecture",
        "difficulty": "expert",
        "prerequisites": ["43.5_q14"],
        "prompt": "Refactor this memory-heavy batch filter into an efficient generator pipeline that yields records on demand in O(1) space:\n\n```python\n# Inefficient eager loading:\ndef filter_logs_eager(lines):\n    results = []\n    for l in lines:\n        if \"ERROR\" in l:\n            results.append(l.strip())\n    return results\n```",
        "starter_code": "def filter_logs_stream(lines):\n    # Implement generator yielding matching lines\n    pass",
        "solution_code": "def filter_logs_stream(lines):\n    for l in lines:\n        if \"ERROR\" in l:\n            yield l.strip()",
        "explanation": "Replacing list building with `yield` produces a generator that evaluates elements lazily, keeping memory consumption constant regardless of file size.",
        "metadata": {
            "concept": "generator_streaming_refactoring",
            "skill": "optimization",
            "learning_objective": "Convert memory-hungry collection accumulators into memory-constant generators",
            "common_misconception": "Building full lists in memory for log processing",
            "why_this_exercise_exists": "Replaces basic code ordering with memory architecture refactoring"
        }
    },
    "43.5_q16": {
        "id": "43.5_q16",
        "type": "output_prediction",
        "concept": "final_mastery_context_manager_protocol",
        "skill": "context_managers",
        "difficulty": "hard",
        "prerequisites": ["43.5_q15"],
        "prompt": "Trace the execution order of this custom context manager:\n\n```python\nclass ManagedResource:\n    def __enter__(self):\n        print(\"1. Acquired\")\n        return self\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        print(\"3. Released\")\n        return True  # Suppresses exception\n\nwith ManagedResource():\n    print(\"2. Working\")\n    raise ValueError(\"Failure\")\nprint(\"4. Finished\")\n```\n\nWhat is the exact output sequence?",
        "options": [
            "1. Acquired\n2. Working\n3. Released\n4. Finished",
            "1. Acquired\n2. Working\nValueError: Failure",
            "1. Acquired\n3. Released\n2. Working\n4. Finished",
            "SyntaxError"
        ],
        "correct_answer": "1. Acquired\n2. Working\n3. Released\n4. Finished",
        "explanation": "`__enter__` runs first (1), then the `with` body executes (2). When `ValueError` is raised, `__exit__` runs (3). Because `__exit__` returns `True`, Python suppresses the exception, allowing execution to continue normally (4).",
        "metadata": {
            "concept": "context_manager_exception_suppression",
            "skill": "advanced_protocols",
            "learning_objective": "Trace context manager lifecycle and exception suppression mechanics",
            "common_misconception": "Believing unhandled exceptions always crash programs inside with blocks",
            "why_this_exercise_exists": "Replaces basic range(3) fill-in with protocol lifecycle tracing"
        }
    },
    "43.5_q17": {
        "id": "43.5_q17",
        "type": "code_prediction",
        "concept": "final_mastery_metaclasses_and_descriptors",
        "skill": "advanced_oop",
        "difficulty": "expert",
        "prerequisites": ["43.5_q16"],
        "prompt": "What design pattern does Python's `@property` decorator implement using dunder methods?",
        "options": [
            "The Descriptor protocol (__get__, __set__, __delete__) to customize attribute access.",
            "The Singleton design pattern.",
            "The Factory pattern.",
            "The Observer protocol."
        ],
        "correct_answer": "The Descriptor protocol (__get__, __set__, __delete__) to customize attribute access.",
        "explanation": "Under the hood, `@property` is a descriptor class implementing `__get__`, `__set__`, and `__delete__`. Descriptors define how attribute access is looked up and managed across Python classes.",
        "metadata": {
            "concept": "descriptor_protocol_architecture",
            "skill": "language_internals",
            "learning_objective": "Recognize that @property is an implementation of Python's descriptor protocol",
            "common_misconception": "Thinking properties are just syntax shortcuts without underlying OOP protocols",
            "why_this_exercise_exists": "Replaces basic function ordering with deep language architecture"
        }
    },
    "43.5_q18": {
        "id": "43.5_q18",
        "type": "write_the_code",
        "concept": "final_mastery_retry_decorator_with_backoff",
        "skill": "production_patterns",
        "difficulty": "expert",
        "prerequisites": ["43.5_q17"],
        "prompt": "Mastery Challenge: Implement a configurable retry decorator `retry(max_attempts=3)` that re-executes a decorated function if it raises an exception. If all attempts fail, re-raise the final exception.",
        "starter_code": "def retry(max_attempts=3):\n    # Build configurable parameterized decorator\n    pass",
        "solution_code": "from functools import wraps\n\ndef retry(max_attempts=3):\n    def decorator(func):\n        @wraps(func)\n        def wrapper(*args, **kwargs):\n            last_err = None\n            for attempt in range(max_attempts):\n                try:\n                    return func(*args, **kwargs)\n                except Exception as e:\n                    last_err = e\n            raise last_err\n        return wrapper\n    return decorator",
        "explanation": "A 3-level nested closure structure creates a parameterized decorator: outer function accepts decorator config (`max_attempts`), middle function accepts `func`, and inner wrapper manages retries with error persistence.",
        "metadata": {
            "concept": "parameterized_retry_decorator",
            "skill": "production_patterns",
            "learning_objective": "Construct parameterized decorators with stateful retry and error propagation",
            "common_misconception": "Swallowing exceptions silently on max failure",
            "why_this_exercise_exists": "Replaces basic negative indexing fill-in with true Python mastery"
        }
    }
}
