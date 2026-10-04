"""
CODOLINGO EXACT REPAIRS: VARIATION FILLER PURGE
Replaces low-effort '(Variation X)' and 'Print(Project: ...)' items in projects:
- 6.8 Number Guessing Game (q8-q12, q26)
- 10.7 Terminal Contact Book (q8-q12)
- 25.6 Weather Dashboard API (q8-q12)
- 27.6 Full-Stack To-Do API (q8-q12, q26)
- 42.2 Data Pipeline (q8-q12)
- 13.1, 14.5, 19.5 placeholder output predictions
"""

REPLACEMENTS_VARIATION_CLEANUP = {
    # ==========================================
    # 6.8 PROJECT: NUMBER GUESSING GAME
    # ==========================================
    "6.8_q8": {
        "id": "6.8_q8",
        "type": "write_the_code",
        "concept": "project_number_guessing_game_secret_generation",
        "skill": "project_milestone",
        "difficulty": "easy",
        "prerequisites": ["6.8_q7"],
        "prompt": "Guessing Game Milestone 1: Generate a random secret integer between 1 and 100 (inclusive) using `random.randint(1, 100)` and store in `secret_number`.",
        "starter_code": "import random\n# Generate secret number between 1 and 100\n",
        "solution_code": "import random\nsecret_number = random.randint(1, 100)\nprint(1 <= secret_number <= 100)",
        "explanation": "`random.randint(a, b)` generates an integer N such that `a <= N <= b`.",
        "metadata": {"concept": "random_int_generation", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with real game secret generation"}
    },
    "6.8_q9": {
        "id": "6.8_q9",
        "type": "write_the_code",
        "concept": "project_number_guessing_game_hint_low",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["6.8_q8"],
        "prompt": "Guessing Game Milestone 2: Given `secret = 42` and user `guess = 30`, write an `if` check that prints `'Too low!'` when `guess < secret`.",
        "starter_code": "secret = 42\nguess = 30\n# Check if guess is too low\n",
        "solution_code": "secret = 42\nguess = 30\nif guess < secret:\n    print(\"Too low!\")",
        "explanation": "Comparing `guess < secret` provides low-guess feedback to guide the player's next attempt.",
        "metadata": {"concept": "game_hint_low", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with low hint branch"}
    },
    "6.8_q10": {
        "id": "6.8_q10",
        "type": "write_the_code",
        "concept": "project_number_guessing_game_hint_high",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["6.8_q9"],
        "prompt": "Guessing Game Milestone 3: Given `secret = 42` and user `guess = 55`, write an `if` check that prints `'Too high!'` when `guess > secret`.",
        "starter_code": "secret = 42\nguess = 55\n# Check if guess is too high\n",
        "solution_code": "secret = 42\nguess = 55\nif guess > secret:\n    print(\"Too high!\")",
        "explanation": "Comparing `guess > secret` signals that the player must guess a smaller number.",
        "metadata": {"concept": "game_hint_high", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with high hint branch"}
    },
    "6.8_q11": {
        "id": "6.8_q11",
        "type": "write_the_code",
        "concept": "project_number_guessing_game_win_condition",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["6.8_q10"],
        "prompt": "Guessing Game Milestone 4: Given `secret = 42` and `guess = 42`, verify equality and set `has_won = True`.",
        "starter_code": "secret = 42\nguess = 42\nhas_won = False\n# Verify win condition\n",
        "solution_code": "secret = 42\nguess = 42\nhas_won = False\nif guess == secret:\n    has_won = True\nprint(f\"Won: {has_won}\")",
        "explanation": "Testing `guess == secret` identifies the win state and terminates the round.",
        "metadata": {"concept": "game_win_condition", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with win condition"}
    },
    "6.8_q12": {
        "id": "6.8_q12",
        "type": "write_the_code",
        "concept": "project_number_guessing_game_attempt_tracker",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["6.8_q11"],
        "prompt": "Guessing Game Milestone 5: Track attempts. Start `attempts = 0`, simulate 3 guesses by incrementing `attempts += 1` inside a loop, and print the total attempts.",
        "starter_code": "attempts = 0\nsimulated_guesses = [10, 50, 42]\n# Count attempts\n",
        "solution_code": "attempts = 0\nsimulated_guesses = [10, 50, 42]\nfor g in simulated_guesses:\n    attempts += 1\nprint(f\"Total attempts: {attempts}\")",
        "explanation": "Tracking attempt count provides score metrics and enforces maximum guess limits.",
        "metadata": {"concept": "attempt_counter", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with attempt counting"}
    },
    "6.8_q26": {
        "id": "6.8_q26",
        "type": "write_the_code",
        "concept": "project_number_guessing_game_full_loop",
        "skill": "project_milestone",
        "difficulty": "hard",
        "prerequisites": ["6.8_q25"],
        "prompt": "Guessing Game Challenge: Build a function `play_game(secret, guesses, max_attempts=5)` that processes guesses sequentially, returning `True` if the player guessed correctly within `max_attempts`, or `False` if attempts were exhausted.",
        "starter_code": "def play_game(secret, guesses, max_attempts=5):\n    # Simulate complete game\n    pass",
        "solution_code": "def play_game(secret, guesses, max_attempts=5):\n    attempts = 0\n    for g in guesses:\n        attempts += 1\n        if g == secret:\n            return True\n        if attempts >= max_attempts:\n            break\n    return False\n\nprint(play_game(42, [10, 20, 42], max_attempts=5))",
        "explanation": "Assembles guess comparison, attempt incrementation, and early-exit conditions into a complete game engine function.",
        "metadata": {"concept": "complete_game_loop", "skill": "project_integration", "why_this_exercise_exists": "Replaces variation with complete game challenge"}
    },

    # ==========================================
    # 10.7 PROJECT: TERMINAL CONTACT BOOK
    # ==========================================
    "10.7_q8": {
        "id": "10.7_q8",
        "type": "write_the_code",
        "concept": "project_terminal_contact_book_init",
        "skill": "project_milestone",
        "difficulty": "easy",
        "prerequisites": ["10.7_q7"],
        "prompt": "Contact Book Milestone 1: Initialize an empty dictionary `contacts = {}` and add a contact `'Alice'` with phone number `'555-0101'`.",
        "starter_code": "# Initialize and add Alice\n",
        "solution_code": "contacts = {}\ncontacts[\"Alice\"] = \"555-0101\"\nprint(contacts)",
        "explanation": "Dictionaries use unique keys (contact names) to store corresponding phone strings.",
        "metadata": {"concept": "contact_dict_insert", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with contact book insertion"}
    },
    "10.7_q9": {
        "id": "10.7_q9",
        "type": "write_the_code",
        "concept": "project_terminal_contact_book_search",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["10.7_q8"],
        "prompt": "Contact Book Milestone 2: Given `contacts = {'Bob': '555-0202'}`, safely look up `'Bob'` and `'Charlie'` using `contacts.get(name, 'Not found')`.",
        "starter_code": "contacts = {\"Bob\": \"555-0202\"}\n# Safe lookup\n",
        "solution_code": "contacts = {\"Bob\": \"555-0202\"}\nprint(contacts.get(\"Bob\", \"Not found\"))\nprint(contacts.get(\"Charlie\", \"Not found\"))",
        "explanation": "`.get()` prevents `KeyError` crashes when searching for unregistered contacts.",
        "metadata": {"concept": "safe_dict_lookup", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with safe contact lookup"}
    },
    "10.7_q10": {
        "id": "10.7_q10",
        "type": "write_the_code",
        "concept": "project_terminal_contact_book_delete",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["10.7_q9"],
        "prompt": "Contact Book Milestone 3: Given `contacts = {'Alice': '555-0101', 'Bob': '555-0202'}`, remove `'Alice'` using `contacts.pop(name, None)`.",
        "starter_code": "contacts = {\"Alice\": \"555-0101\", \"Bob\": \"555-0202\"}\n# Delete Alice\n",
        "solution_code": "contacts = {\"Alice\": \"555-0101\", \"Bob\": \"555-0202\"}\nremoved = contacts.pop(\"Alice\", None)\nprint(f\"Removed: {removed}, Remaining: {list(contacts.keys())}\")",
        "explanation": "Calling `.pop(key, None)` deletes the key if present without raising an error if it doesn't exist.",
        "metadata": {"concept": "safe_dict_deletion", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with safe contact deletion"}
    },
    "10.7_q11": {
        "id": "10.7_q11",
        "type": "write_the_code",
        "concept": "project_terminal_contact_book_list_sorted",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["10.7_q10"],
        "prompt": "Contact Book Milestone 4: Given `contacts = {'Zara': '555-9999', 'Adam': '555-1111'}`, print each contact formatted as `'Name: Phone'` sorted alphabetically by name.",
        "starter_code": "contacts = {\"Zara\": \"555-9999\", \"Adam\": \"555-1111\"}\n# Print sorted\n",
        "solution_code": "contacts = {\"Zara\": \"555-9999\", \"Adam\": \"555-1111\"}\nfor name in sorted(contacts.keys()):\n    print(f\"{name}: {contacts[name]}\")",
        "explanation": "Iterating over `sorted(contacts.keys())` presents contact directories in clean alphabetical order.",
        "metadata": {"concept": "sorted_contact_listing", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with sorted contact roster"}
    },
    "10.7_q12": {
        "id": "10.7_q12",
        "type": "write_the_code",
        "concept": "project_terminal_contact_book_update",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["10.7_q11"],
        "prompt": "Contact Book Milestone 5: Update an existing contact's phone number or insert if new. Update `'Adam'` to `'555-2222'` in `contacts`.",
        "starter_code": "contacts = {\"Adam\": \"555-1111\"}\n# Update phone number\n",
        "solution_code": "contacts = {\"Adam\": \"555-1111\"}\ncontacts[\"Adam\"] = \"555-2222\"\nprint(contacts[\"Adam\"])",
        "explanation": "Assigning to an existing dictionary key overwrites the old value in place.",
        "metadata": {"concept": "dict_in_place_update", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with contact update"}
    },

    # ==========================================
    # 25.6 PROJECT: API WEATHER DASHBOARD
    # ==========================================
    "25.6_q8": {
        "id": "25.6_q8",
        "type": "write_the_code",
        "concept": "project_api_weather_dashboard_temp_extract",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["25.6_q7"],
        "prompt": "Weather Dashboard Milestone 1: Extract temperature. Given API response payload `payload = {'main': {'temp': 295.15, 'humidity': 60}}`, extract temperature into `temp_k`.",
        "starter_code": "payload = {\"main\": {\"temp\": 295.15, \"humidity\": 60}}\n# Extract temp\n",
        "solution_code": "payload = {\"main\": {\"temp\": 295.15, \"humidity\": 60}}\ntemp_k = payload[\"main\"][\"temp\"]\nprint(f\"Kelvin: {temp_k}\")",
        "explanation": "Navigating nested JSON dictionaries via `payload['main']['temp']` extracts weather readings.",
        "metadata": {"concept": "nested_json_extraction", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with temperature parsing"}
    },
    "25.6_q9": {
        "id": "25.6_q9",
        "type": "write_the_code",
        "concept": "project_api_weather_dashboard_kelvin_to_celsius",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["25.6_q8"],
        "prompt": "Weather Dashboard Milestone 2: Convert temperature from Kelvin `295.15` to Celsius (`temp_k - 273.15`) rounded to 1 decimal place into `temp_c`.",
        "starter_code": "temp_k = 295.15\n# Convert to Celsius\n",
        "solution_code": "temp_k = 295.15\ntemp_c = round(temp_k - 273.15, 1)\nprint(f\"Celsius: {temp_c}°C\")",
        "explanation": "Subtracting 273.15 converts standard Kelvin readings into user-friendly Celsius format (`22.0°C`).",
        "metadata": {"concept": "temperature_conversion", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with metric conversion"}
    },
    "25.6_q10": {
        "id": "25.6_q10",
        "type": "write_the_code",
        "concept": "project_api_weather_dashboard_desc_extract",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["25.6_q9"],
        "prompt": "Weather Dashboard Milestone 3: Extract weather condition description from `payload = {'weather': [{'description': 'clear sky'}]}` into variable `description`.",
        "starter_code": "payload = {\"weather\": [{\"description\": \"clear sky\"}]}\n# Extract description\n",
        "solution_code": "payload = {\"weather\": [{\"description\": \"clear sky\"}]}\ndescription = payload[\"weather\"][0][\"description\"]\nprint(description.title())",
        "explanation": "The `weather` key contains a list of condition dicts; accessing index `0` extracts the primary description.",
        "metadata": {"concept": "nested_list_dict_navigation", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with description extraction"}
    },
    "25.6_q11": {
        "id": "25.6_q11",
        "type": "write_the_code",
        "concept": "project_api_weather_dashboard_http_status",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["25.6_q10"],
        "prompt": "Weather Dashboard Milestone 4: Verify HTTP response status. Given `status_code = 200`, write an `if-else` check: if 200 print `'Success'`, else print `f'API Error: {status_code}'`.",
        "starter_code": "status_code = 200\n# Check status code\n",
        "solution_code": "status_code = 200\nif status_code == 200:\n    print(\"Success\")\nelse:\n    print(f\"API Error: {status_code}\")",
        "explanation": "Checking HTTP status codes prevents downstream JSON parsing crashes when requests fail.",
        "metadata": {"concept": "http_status_guard", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with API status check"}
    },
    "25.6_q12": {
        "id": "25.6_q12",
        "type": "write_the_code",
        "concept": "project_api_weather_dashboard_city_not_found",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["25.6_q11"],
        "prompt": "Weather Dashboard Milestone 5: Handle missing city (HTTP 404). Given `status_code = 404`, set `error_msg = 'City not found. Please verify spelling.'`.",
        "starter_code": "status_code = 404\nerror_msg = \"\"\n# Handle 404\n",
        "solution_code": "status_code = 404\nerror_msg = \"\"\nif status_code == 404:\n    error_msg = \"City not found. Please verify spelling.\"\nprint(error_msg)",
        "explanation": "Providing actionable, human-readable error messages when endpoints return 404 improves user experience.",
        "metadata": {"concept": "client_error_reporting", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with 404 handling"}
    },

    # ==========================================
    # 27.6 PROJECT: FULL-STACK TO-DO API
    # ==========================================
    "27.6_q8": {
        "id": "27.6_q8",
        "type": "write_the_code",
        "concept": "project_full_stack_to_do_api_model_init",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["27.6_q7"],
        "prompt": "To-Do API Milestone 1: Initialize in-memory task database `todos = {}` and task ID counter `next_id = 1`.",
        "starter_code": "# Initialize todos and counter\n",
        "solution_code": "todos = {}\nnext_id = 1\nprint(f\"Initialized API with {len(todos)} tasks\")",
        "explanation": "Establishes state storage for incoming CRUD operations.",
        "metadata": {"concept": "api_storage_init", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with to-do API storage init"}
    },
    "27.6_q9": {
        "id": "27.6_q9",
        "type": "write_the_code",
        "concept": "project_full_stack_to_do_api_create_task",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["27.6_q8"],
        "prompt": "To-Do API Milestone 2: Create task. Given `title = 'Buy groceries'`, create task record `{'id': 1, 'title': title, 'completed': False}` and store in `todos[1]`.",
        "starter_code": "todos = {}\ntitle = \"Buy groceries\"\n# Create task\n",
        "solution_code": "todos = {}\ntitle = \"Buy groceries\"\ntask = {\"id\": 1, \"title\": title, \"completed\": False}\ntodos[1] = task\nprint(todos[1])",
        "explanation": "Creates a structured entity record with default completion state `False`.",
        "metadata": {"concept": "create_task_entity", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with task creation"}
    },
    "27.6_q10": {
        "id": "27.6_q10",
        "type": "write_the_code",
        "concept": "project_full_stack_to_do_api_toggle_status",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["27.6_q9"],
        "prompt": "To-Do API Milestone 3: Toggle task completion. Given `task = {'id': 1, 'completed': False}`, toggle `task['completed']` using boolean `not`.",
        "starter_code": "task = {\"id\": 1, \"completed\": False}\n# Toggle completed\n",
        "solution_code": "task = {\"id\": 1, \"completed\": False}\ntask[\"completed\"] = not task[\"completed\"]\nprint(f\"Task 1 completed: {task['completed']}\")",
        "explanation": "`task['completed'] = not task['completed']` flips `False` to `True` or `True` to `False`.",
        "metadata": {"concept": "toggle_entity_state", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with status toggle"}
    },
    "27.6_q11": {
        "id": "27.6_q11",
        "type": "write_the_code",
        "concept": "project_full_stack_to_do_api_delete_task",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["27.6_q10"],
        "prompt": "To-Do API Milestone 4: Delete task by ID. Given `todos = {1: {'title': 'Task 1'}}`, delete task with ID `1` using `todos.pop(1, None)`.",
        "starter_code": "todos = {1: {\"title\": \"Task 1\"}}\n# Delete task 1\n",
        "solution_code": "todos = {1: {\"title\": \"Task 1\"}}\ndeleted = todos.pop(1, None)\nprint(f\"Deleted: {deleted}, Remaining: {len(todos)}\")",
        "explanation": "Popping removes the item from the dictionary and returns it for response confirmation.",
        "metadata": {"concept": "delete_entity_by_id", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with task deletion"}
    },
    "27.6_q12": {
        "id": "27.6_q12",
        "type": "write_the_code",
        "concept": "project_full_stack_to_do_api_list_filter",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["27.6_q11"],
        "prompt": "To-Do API Milestone 5: Filter tasks. Given `todos = {1: {'completed': True}, 2: {'completed': False}}`, return all pending (uncompleted) tasks in list `pending`.",
        "starter_code": "todos = {1: {\"completed\": True}, 2: {\"completed\": False}}\n# Filter pending\n",
        "solution_code": "todos = {1: {\"completed\": True}, 2: {\"completed\": False}}\npending = [t for t in todos.values() if not t[\"completed\"]]\nprint(f\"Pending tasks count: {len(pending)}\")",
        "explanation": "List comprehensions filter dictionary values by status flags in linear O(n) time.",
        "metadata": {"concept": "filter_tasks_by_status", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with task filtering"}
    },
    "27.6_q26": {
        "id": "27.6_q26",
        "type": "write_the_code",
        "concept": "project_full_stack_to_do_api_crud_manager",
        "skill": "system_design",
        "difficulty": "hard",
        "prerequisites": ["27.6_q25"],
        "prompt": "To-Do API Challenge: Implement a class `TodoManager` with methods `add_task(title)`, `get_task(task_id)`, `toggle_task(task_id)`, and `delete_task(task_id)`.",
        "starter_code": "class TodoManager:\n    # Implement complete CRUD manager\n    pass",
        "solution_code": "class TodoManager:\n    def __init__(self):\n        self.todos = {}\n        self.next_id = 1\n    def add_task(self, title):\n        tid = self.next_id\n        self.todos[tid] = {\"id\": tid, \"title\": title, \"completed\": False}\n        self.next_id += 1\n        return self.todos[tid]\n    def get_task(self, task_id):\n        return self.todos.get(task_id)\n    def toggle_task(self, task_id):\n        if task_id in self.todos:\n            self.todos[task_id][\"completed\"] = not self.todos[task_id][\"completed\"]\n            return self.todos[task_id]\n        return None\n    def delete_task(self, task_id):\n        return self.todos.pop(task_id, None)\n\nmgr = TodoManager()\nt = mgr.add_task(\"Study Python\")\nprint(mgr.toggle_task(t[\"id\"]))",
        "explanation": "Encapsulates end-to-end CRUD operations, state persistence, and autoincrement ID generation into a reusable manager class.",
        "metadata": {"concept": "full_crud_service_class", "skill": "system_design", "why_this_exercise_exists": "Replaces variation with complete to-do backend class"}
    },

    # 14.6 Expense Tracker milestones
    "14.6_q8": {
        "id": "14.6_q8",
        "type": "write_the_code",
        "concept": "project_cli_expense_tracker_record_creation",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["14.6_q7"],
        "prompt": "Expense Tracker Milestone: Write a function `create_expense(category, amount, note)` that returns a clean dictionary record with keys `category`, `amount` (as float), and `note`.",
        "starter_code": "def create_expense(category, amount, note=\"\"):\n    pass",
        "solution_code": "def create_expense(category, amount, note=\"\"):\n    return {\"category\": category, \"amount\": float(amount), \"note\": note}\n\nprint(create_expense(\"Food\", 12.50))",
        "explanation": "Standardizes expense entity creation with proper float typing.",
        "metadata": {"concept": "expense_entity_constructor", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with expense entity builder"}
    },
    "14.6_q9": {
        "id": "14.6_q9",
        "type": "write_the_code",
        "concept": "project_cli_expense_tracker_listing",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["14.6_q8"],
        "prompt": "Expense Tracker Milestone: Given `expenses = [{'category': 'Gas', 'amount': 40.0}]`, format and print each entry as `'Category: $Amount'`.",
        "starter_code": "expenses = [{\"category\": \"Gas\", \"amount\": 40.0}]\n# Format and display\n",
        "solution_code": "expenses = [{\"category\": \"Gas\", \"amount\": 40.0}]\nfor e in expenses:\n    print(f\"{e['category']}: ${e['amount']:.2f}\")",
        "explanation": "Formats monetary amounts with two decimal places for clear CLI viewing.",
        "metadata": {"concept": "expense_table_display", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with expense roster display"}
    },
    "14.6_q11": {
        "id": "14.6_q11",
        "type": "write_the_code",
        "concept": "project_cli_expense_tracker_category_breakdown",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["14.6_q10"],
        "prompt": "Expense Tracker Milestone: Group spending by category. Given `expenses = [{'category': 'A', 'amount': 10}, {'category': 'B', 'amount': 20}, {'category': 'A', 'amount': 15}]`, return a dictionary mapping category to total spend.",
        "starter_code": "expenses = [{\"category\": \"A\", \"amount\": 10}, {\"category\": \"B\", \"amount\": 20}, {\"category\": \"A\", \"amount\": 15}]\nbreakdown = {}\n# Compute category breakdown\n",
        "solution_code": "expenses = [{\"category\": \"A\", \"amount\": 10}, {\"category\": \"B\", \"amount\": 20}, {\"category\": \"A\", \"amount\": 15}]\nbreakdown = {}\nfor e in expenses:\n    breakdown[e[\"category\"]] = breakdown.get(e[\"category\"], 0) + e[\"amount\"]\nprint(breakdown)",
        "explanation": "Aggregates expenditures per category using `dict.get()`.",
        "metadata": {"concept": "category_breakdown", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with category expenditure aggregation"}
    },
    "14.6_q12": {
        "id": "14.6_q12",
        "type": "write_the_code",
        "concept": "project_cli_expense_tracker_persistence",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["14.6_q11"],
        "prompt": "Expense Tracker Milestone: Save expenses to JSON. Given `expenses = [{'category': 'Food', 'amount': 15.0}]`, serialize and write to `'expenses.json'` using `json.dump`.",
        "starter_code": "import json\nexpenses = [{\"category\": \"Food\", \"amount\": 15.0}]\n# Save to expenses.json\n",
        "solution_code": "import json\nexpenses = [{\"category\": \"Food\", \"amount\": 15.0}]\nwith open(\"expenses.json\", \"w\") as f:\n    json.dump(expenses, f, indent=2)",
        "explanation": "Persisting structured expenses to disk ensures state survives across application restarts.",
        "metadata": {"concept": "json_expense_persistence", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with file persistence"}
    },
    "14.6_q26": {
        "id": "14.6_q26",
        "type": "write_the_code",
        "concept": "project_cli_expense_tracker_full_suite",
        "skill": "system_design",
        "difficulty": "hard",
        "prerequisites": ["14.6_q25"],
        "prompt": "Expense Tracker Challenge: Implement `ExpenseTracker` class with methods `add_expense(category, amount)`, `get_total()`, and `get_category_total(category)`.",
        "starter_code": "class ExpenseTracker:\n    # Implement expense tracker system\n    pass",
        "solution_code": "class ExpenseTracker:\n    def __init__(self):\n        self.expenses = []\n    def add_expense(self, category, amount):\n        self.expenses.append({\"category\": category, \"amount\": float(amount)})\n    def get_total(self):\n        return sum(e[\"amount\"] for e in self.expenses)\n    def get_category_total(self, category):\n        return sum(e[\"amount\"] for e in self.expenses if e[\"category\"] == category)\n\ntracker = ExpenseTracker()\ntracker.add_expense(\"Food\", 25.50)\nprint(tracker.get_total())",
        "explanation": "Consolidates expense recording and multi-dimensional aggregations into an object-oriented tracker.",
        "metadata": {"concept": "expense_tracker_oop_class", "skill": "system_design", "why_this_exercise_exists": "Replaces variation with full tracker class"}
    },

    # 42.2 Data Pipeline milestones (q8-q12)
    "42.2_q8": {
        "id": "42.2_q8",
        "type": "write_the_code",
        "concept": "project_data_pipeline_deduplication",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q7"],
        "prompt": "Pipeline Milestone: Deduplicate rows by `'id'`. Given `records = [{'id': 1, 'val': 10}, {'id': 1, 'val': 10}, {'id': 2, 'val': 20}]`, filter out duplicate IDs preserving first occurrence in `deduped`.",
        "starter_code": "records = [{\"id\": 1, \"val\": 10}, {\"id\": 1, \"val\": 10}, {\"id\": 2, \"val\": 20}]\n# Deduplicate records\n",
        "solution_code": "records = [{\"id\": 1, \"val\": 10}, {\"id\": 1, \"val\": 10}, {\"id\": 2, \"val\": 20}]\nseen = set()\ndeduped = []\nfor r in records:\n    if r[\"id\"] not in seen:\n        seen.add(r[\"id\"])\n        deduped.append(r)\nprint(f\"Deduplicated: {len(deduped)} rows\")",
        "explanation": "Using a `seen` set checks presence in O(1) time and preserves row order.",
        "metadata": {"concept": "row_deduplication", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with data deduplication"}
    },
    "42.2_q9": {
        "id": "42.2_q9",
        "type": "write_the_code",
        "concept": "project_data_pipeline_null_imputation",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q8"],
        "prompt": "Pipeline Milestone: Impute missing values. Given `values = [10.0, None, 20.0, None]`, compute the mean of non-null values and replace `None` entries with the mean.",
        "starter_code": "values = [10.0, None, 20.0, None]\n# Impute missing values with mean\n",
        "solution_code": "values = [10.0, None, 20.0, None]\nvalid = [v for v in values if v is not None]\nmean_val = sum(valid) / len(valid)\nimputed = [v if v is not None else mean_val for v in values]\nprint(imputed)",
        "explanation": "Imputes missing values with dataset averages, preserving distribution.",
        "metadata": {"concept": "missing_value_imputation", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with data cleaning imputation"}
    },
    "42.2_q10": {
        "id": "42.2_q10",
        "type": "write_the_code",
        "concept": "project_data_pipeline_monthly_aggregation",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q9"],
        "prompt": "Pipeline Milestone: Group sales by month. Given `txs = [{'date': '2026-01-15', 'amt': 100}, {'date': '2026-01-20', 'amt': 50}, {'date': '2026-02-01', 'amt': 80}]`, aggregate sales by month `YYYY-MM`.",
        "starter_code": "txs = [{\"date\": \"2026-01-15\", \"amt\": 100}, {\"date\": \"2026-01-20\", \"amt\": 50}, {\"date\": \"2026-02-01\", \"amt\": 80}]\n# Aggregate by month\n",
        "solution_code": "txs = [{\"date\": \"2026-01-15\", \"amt\": 100}, {\"date\": \"2026-01-20\", \"amt\": 50}, {\"date\": \"2026-02-01\", \"amt\": 80}]\nmonthly = {}\nfor t in txs:\n    month = t[\"date\"][:7]\n    monthly[month] = monthly.get(month, 0) + t[\"amt\"]\nprint(monthly)",
        "explanation": "Slicing date string `[:7]` extracts `YYYY-MM` as aggregation buckets.",
        "metadata": {"concept": "temporal_aggregation", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with monthly aggregation"}
    },
    "42.2_q11": {
        "id": "42.2_q11",
        "type": "write_the_code",
        "concept": "project_data_pipeline_csv_export",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q10"],
        "prompt": "Pipeline Milestone: Export cleaned records `records = [{'id': 1, 'name': 'Aria'}]` to CSV using `csv.DictWriter`.",
        "starter_code": "import csv\nrecords = [{\"id\": 1, \"name\": \"Aria\"}]\n# Export to clean_data.csv\n",
        "solution_code": "import csv\nfrom io import StringIO\nrecords = [{\"id\": 1, \"name\": \"Aria\"}]\nout = StringIO()\nwriter = csv.DictWriter(out, fieldnames=[\"id\", \"name\"])\nwriter.writeheader()\nwriter.writerows(records)\nprint(out.getvalue())",
        "explanation": "`csv.DictWriter` ensures proper quoting and header alignment in exported files.",
        "metadata": {"concept": "csv_export_pipeline", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with CSV exporter"}
    },
    "42.2_q12": {
        "id": "42.2_q12",
        "type": "write_the_code",
        "concept": "project_data_pipeline_telemetry_metrics",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["42.2_q11"],
        "prompt": "Pipeline Milestone: Generate audit metrics. Write a summary dict `{'input_rows': 100, 'valid_rows': 95, 'dropped_rows': 5}` logging pipeline throughput.",
        "starter_code": "# Generate pipeline audit metrics\n",
        "solution_code": "def generate_audit_metrics(raw_count, clean_count):\n    return {\n        \"input_rows\": raw_count,\n        \"valid_rows\": clean_count,\n        \"dropped_rows\": raw_count - clean_count\n    }\nprint(generate_audit_metrics(100, 95))",
        "explanation": "Logging input, output, and dropped records provides production pipeline observability.",
        "metadata": {"concept": "pipeline_audit_telemetry", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with pipeline telemetry"}
    },

    # 42.3 Web Scraper API challenges (q26-q30)
    "42.3_q26": {
        "id": "42.3_q26",
        "type": "write_the_code",
        "concept": "project_web_scraper_api_rate_limiting",
        "skill": "api_security",
        "difficulty": "hard",
        "prerequisites": ["42.3_q25"],
        "prompt": "Scraper API Milestone: Implement client rate limiting. Given client IP `'192.168.1.1'`, allow up to 3 requests per client using an in-memory dictionary counter `request_counts`.",
        "starter_code": "request_counts = {}\n# Track and limit client requests\n",
        "solution_code": "request_counts = {}\ndef allow_request(ip, limit=3):\n    current = request_counts.get(ip, 0)\n    if current >= limit:\n        return False\n    request_counts[ip] = current + 1\n    return True\nprint(allow_request(\"192.168.1.1\"))",
        "explanation": "Guards backend scrapers against abuse and denial-of-service surges.",
        "metadata": {"concept": "rate_limiting_guard", "skill": "api_security", "why_this_exercise_exists": "Replaces variation with API rate limiter"}
    },
    "42.3_q27": {
        "id": "42.3_q27",
        "type": "write_the_code",
        "concept": "project_web_scraper_api_exponential_backoff",
        "skill": "networking",
        "difficulty": "hard",
        "prerequisites": ["42.3_q26"],
        "prompt": "Scraper API Milestone: Exponential backoff calculation. Write a function `get_backoff_delay(attempt, base_delay=1)` that calculates exponential backoff delay (`base_delay * 2 ** attempt`).",
        "starter_code": "def get_backoff_delay(attempt, base_delay=1):\n    pass",
        "solution_code": "def get_backoff_delay(attempt, base_delay=1):\n    return base_delay * (2 ** attempt)\n\nprint([get_backoff_delay(i) for i in range(4)])",
        "explanation": "Exponential backoff doubles wait times between retries to avoid overwhelming target servers.",
        "metadata": {"concept": "exponential_backoff", "skill": "networking", "why_this_exercise_exists": "Replaces variation with exponential backoff algorithm"}
    },
    "42.3_q28": {
        "id": "42.3_q28",
        "type": "write_the_code",
        "concept": "project_web_scraper_api_opengraph_extract",
        "skill": "scraping",
        "difficulty": "hard",
        "prerequisites": ["42.3_q27"],
        "prompt": "Scraper API Milestone: Extract OpenGraph metadata. From HTML `html = '<meta property=\"og:title\" content=\"My Article\">'`, extract the `content` attribute using BeautifulSoup.",
        "starter_code": "from bs4 import BeautifulSoup\nhtml = '<meta property=\"og:title\" content=\"My Article\">'\n# Extract og:title content\n",
        "solution_code": "from bs4 import BeautifulSoup\nhtml = '<meta property=\"og:title\" content=\"My Article\">'\nsoup = BeautifulSoup(html, \"html.parser\")\ntag = soup.find(\"meta\", property=\"og:title\")\nog_title = tag[\"content\"] if tag else \"\"\nprint(og_title)",
        "explanation": "Targeting `<meta property=\"og:...\">` tags extracts social sharing metadata from pages.",
        "metadata": {"concept": "opengraph_tag_scraping", "skill": "scraping", "why_this_exercise_exists": "Replaces variation with OpenGraph extraction"}
    },
    "42.3_q29": {
        "id": "42.3_q29",
        "type": "write_the_code",
        "concept": "project_web_scraper_api_test_client",
        "skill": "testing",
        "difficulty": "hard",
        "prerequisites": ["42.3_q28"],
        "prompt": "Scraper API Milestone: Automated route testing. Write a test function `test_health_route()` that asserts `health_endpoint()` returns status 200 and `{'status': 'healthy'}`.",
        "starter_code": "def health_endpoint():\n    return 200, {\"status\": \"healthy\"}\n\ndef test_health_route():\n    # Assert status and body\n    pass",
        "solution_code": "def health_endpoint():\n    return 200, {\"status\": \"healthy\"}\n\ndef test_health_route():\n    status, body = health_endpoint()\n    assert status == 200\n    assert body[\"status\"] == \"healthy\"\n\ntest_health_route()\nprint(\"Health test passed\")",
        "explanation": "Unit testing endpoint handlers ensures API contracts remain unbroken during updates.",
        "metadata": {"concept": "api_unit_testing", "skill": "testing", "why_this_exercise_exists": "Replaces variation with API test client assertions"}
    },
    "42.3_q30": {
        "id": "42.3_q30",
        "type": "write_the_code",
        "concept": "project_web_scraper_api_full_engine",
        "skill": "system_design",
        "difficulty": "expert",
        "prerequisites": ["42.3_q29"],
        "prompt": "Capstone Project Mastery: Build the consolidated `scrape_and_structure_page(html, target_url)` pipeline function that validates inputs, extracts `<title>`, all `<h2>` headings, and image `<img src=...>` links into a clean structured dictionary.",
        "starter_code": "from bs4 import BeautifulSoup\n\ndef scrape_and_structure_page(html, target_url):\n    # Complete scraping engine\n    pass",
        "solution_code": "from bs4 import BeautifulSoup\n\ndef scrape_and_structure_page(html, target_url):\n    if not html:\n        return {\"url\": target_url, \"error\": \"Empty response\"}\n    soup = BeautifulSoup(html, \"html.parser\")\n    title_tag = soup.find(\"title\")\n    title = title_tag.text.strip() if title_tag else \"Untitled\"\n    headings = [h.text.strip() for h in soup.find_all(\"h2\")]\n    images = [img[\"src\"] for img in soup.find_all(\"img\") if img.get(\"src\")]\n    return {\n        \"url\": target_url,\n        \"title\": title,\n        \"headings\": headings,\n        \"images\": images\n    }\n\nhtml = \"<html><head><title>Portfolio</title></head><body><h2>Work</h2><img src='logo.png'></body></html>\"\nprint(scrape_and_structure_page(html, \"https://example.com\"))",
        "explanation": "Consolidates HTML parsing, null checks, multiple tag extractions, and API packaging into a complete web scraper pipeline.",
        "metadata": {"concept": "full_scraper_pipeline", "skill": "system_design", "why_this_exercise_exists": "Replaces variation with full capstone scraper engine"}
    },

    # 7.9 String Formatter milestones (q8-q12)
    "7.9_q8": {
        "id": "7.9_q8",
        "type": "write_the_code",
        "concept": "project_string_formatter_strip_punctuation",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q7"],
        "prompt": "Formatter Milestone: Strip trailing punctuation. Given `raw_text = 'Hello, world!!!'`, strip trailing exclamation marks and commas using `raw_text.rstrip('!,')`.",
        "starter_code": "raw_text = \"Hello, world!!!\"\n# Strip trailing punctuation\n",
        "solution_code": "raw_text = \"Hello, world!!!\"\nclean_text = raw_text.rstrip(\"!,\")\nprint(clean_text)",
        "explanation": "`rstrip('!,')` removes any trailing commas or exclamation points from the string's right end.",
        "metadata": {"concept": "punctuation_stripping", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with punctuation stripping"}
    },
    "7.9_q9": {
        "id": "7.9_q9",
        "type": "write_the_code",
        "concept": "project_string_formatter_slug_to_text",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q8"],
        "prompt": "Formatter Milestone: Convert slug to title. Given `slug = 'python_programming_fundamentals'`, replace underscores with spaces and capitalize each word in Title Case.",
        "starter_code": "slug = \"python_programming_fundamentals\"\n# Convert to title\n",
        "solution_code": "slug = \"python_programming_fundamentals\"\ntitle = slug.replace(\"_\", \" \").title()\nprint(title)",
        "explanation": "Chaining `.replace('_', ' ')` and `.title()` converts snake_case slugs into clean document titles.",
        "metadata": {"concept": "slug_conversion", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with slug conversion"}
    },
    "7.9_q10": {
        "id": "7.9_q10",
        "type": "write_the_code",
        "concept": "project_string_formatter_currency_commas",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q9"],
        "prompt": "Formatter Milestone: Format currency with comma thousand-separators. Given `amount = 1250000.75`, format into `f'${amount:,.2f}'`.",
        "starter_code": "amount = 1250000.75\n# Format with comma separators\n",
        "solution_code": "amount = 1250000.75\nformatted = f\"${amount:,.2f}\"\nprint(formatted)",
        "explanation": "Format specifier `:,` adds comma separators every three digits, and `.2f` fixes two decimal places (`$1,250,000.75`).",
        "metadata": {"concept": "currency_formatting", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with currency formatting"}
    },
    "7.9_q11": {
        "id": "7.9_q11",
        "type": "write_the_code",
        "concept": "project_string_formatter_pad_columns",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q10"],
        "prompt": "Formatter Milestone: Align text into tabular columns. Pad string `'Invoice'` to width 15 left-aligned using `.ljust(15)` and append amount `'$450.00'`.",
        "starter_code": "label = \"Invoice\"\namount = \"$450.00\"\n# Left-align label to width 15\n",
        "solution_code": "label = \"Invoice\"\namount = \"$450.00\"\nline = f\"{label.ljust(15)}{amount}\"\nprint(line)",
        "explanation": "`.ljust(15)` pads spaces to the right, creating clean columnar terminal tables.",
        "metadata": {"concept": "columnar_padding", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with column alignment"}
    },
    "7.9_q12": {
        "id": "7.9_q12",
        "type": "write_the_code",
        "concept": "project_string_formatter_percentage_display",
        "skill": "project_milestone",
        "difficulty": "medium",
        "prerequisites": ["7.9_q11"],
        "prompt": "Formatter Milestone: Format a decimal ratio `ratio = 0.8546` into a percentage with 1 decimal place using `f'{ratio:.1%}'`.",
        "starter_code": "ratio = 0.8546\n# Format percentage\n",
        "solution_code": "ratio = 0.8546\npercentage = f\"{ratio:.1%}\"\nprint(percentage)",
        "explanation": "The `%` format specifier multiplies by 100 and appends `%`, displaying `'85.5%'`.",
        "metadata": {"concept": "percentage_formatting", "skill": "project_milestone", "why_this_exercise_exists": "Replaces variation with percentage formatting"}
    },

    # 13.1 Reading Text Files (q8, q9, q11, q12)
    "13.1_q8": {
        "id": "13.1_q8",
        "type": "output_prediction",
        "concept": "reading_text_files_word_count",
        "skill": "file_analytics",
        "difficulty": "medium",
        "prerequisites": ["13.1_q7"],
        "prompt": "How do you count total words in a text file after calling `content = f.read()`?\n\n```python\ntext = \"Python makes coding fun and productive\"\nwords = text.split()\nprint(len(words))\n```",
        "options": ["6", "7", "39", "1"],
        "correct_answer": "6",
        "explanation": "Splitting the text by whitespace with `.split()` generates a list of words; `len()` counts them.",
        "metadata": {"concept": "word_counting_from_file", "skill": "file_analytics", "why_this_exercise_exists": "Replaces variation with word counting"}
    },
    "13.1_q9": {
        "id": "13.1_q9",
        "type": "output_prediction",
        "concept": "reading_text_files_line_count",
        "skill": "file_analytics",
        "difficulty": "medium",
        "prerequisites": ["13.1_q8"],
        "prompt": "What does `len(lines)` return when reading three lines from a file?\n\n```python\ntext = \"Line 1\\nLine 2\\nLine 3\"\nlines = text.splitlines()\nprint(len(lines))\n```",
        "options": ["3", "1", "18", "TypeError"],
        "correct_answer": "3",
        "explanation": "`splitlines()` splits on newline boundaries, returning a list of 3 line elements.",
        "metadata": {"concept": "line_counting_from_file", "skill": "file_analytics", "why_this_exercise_exists": "Replaces variation with line counting"}
    },
    "13.1_q11": {
        "id": "13.1_q11",
        "type": "code_prediction",
        "concept": "reading_text_files_chunking",
        "skill": "chunk_reading",
        "difficulty": "medium",
        "prerequisites": ["13.1_q10"],
        "prompt": "What does passing an integer size to `f.read(10)` do?",
        "options": [
            "Reads at most 10 characters (or bytes in binary mode) from the current file position.",
            "Reads the 10th line of the file.",
            "Skips the first 10 bytes.",
            "Reads 10 whole files."
        ],
        "correct_answer": "Reads at most 10 characters (or bytes in binary mode) from the current file position.",
        "explanation": "Passing an argument `N` to `f.read(N)` reads at most `N` characters, enabling memory-efficient buffered chunk reading.",
        "metadata": {"concept": "chunked_buffer_read", "skill": "chunk_reading", "why_this_exercise_exists": "Replaces variation with chunk reading"}
    },
    "13.1_q12": {
        "id": "13.1_q12",
        "type": "code_prediction",
        "concept": "reading_text_files_seek_reset",
        "skill": "file_pointers",
        "difficulty": "medium",
        "prerequisites": ["13.1_q11"],
        "prompt": "How do you reset the file pointer back to the beginning of the file after reading it?",
        "options": [
            "f.seek(0)",
            "f.reset()",
            "f.rewind()",
            "f.read(0)"
        ],
        "correct_answer": "f.seek(0)",
        "explanation": "`f.seek(0)` positions the internal file read/write offset back to index 0 (the beginning of the file).",
        "metadata": {"concept": "file_seek_pointer", "skill": "file_pointers", "why_this_exercise_exists": "Replaces variation with seek mechanics"}
    },

    # 14.5 Generating JSON (q8, q9, q11, q12)
    "14.5_q8": {
        "id": "14.5_q8",
        "type": "output_prediction",
        "concept": "generating_json_sort_keys",
        "skill": "json_formatting",
        "difficulty": "medium",
        "prerequisites": ["14.5_q7"],
        "prompt": "What does passing `sort_keys=True` to `json.dumps()` accomplish?\n\n```python\nimport json\nd = {\"z\": 1, \"a\": 2}\nprint(json.dumps(d, sort_keys=True))\n```",
        "options": [
            "{\"a\": 2, \"z\": 1}",
            "{\"z\": 1, \"a\": 2}",
            "['a', 'z']",
            "None"
        ],
        "correct_answer": "{\"a\": 2, \"z\": 1}",
        "explanation": "`sort_keys=True` sorts all dictionary keys in alphabetical order, ensuring deterministic JSON output across test runs.",
        "metadata": {"concept": "json_sort_keys_deterministic", "skill": "json_formatting", "why_this_exercise_exists": "Replaces variation with deterministic JSON formatting"}
    },
    "14.5_q9": {
        "id": "14.5_q9",
        "type": "code_prediction",
        "concept": "generating_json_compact",
        "skill": "optimization",
        "difficulty": "medium",
        "prerequisites": ["14.5_q8"],
        "prompt": "How do you produce the most compact JSON string with all whitespace stripped for network transport?",
        "options": [
            "json.dumps(data, separators=(',', ':'))",
            "json.dumps(data, compact=True)",
            "json.dumps(data, indent=0)",
            "json.dumps(data).strip()"
        ],
        "correct_answer": "json.dumps(data, separators=(',', ':'))",
        "explanation": "Overriding `separators=(',', ':')` eliminates default spaces after commas and colons, minimizing payload byte size.",
        "metadata": {"concept": "compact_json_serialization", "skill": "optimization", "why_this_exercise_exists": "Replaces variation with compact JSON transport"}
    },
    "14.5_q11": {
        "id": "14.5_q11",
        "type": "write_the_code",
        "concept": "generating_json_dump_to_file",
        "skill": "file_io",
        "difficulty": "medium",
        "prerequisites": ["14.5_q10"],
        "prompt": "Write a snippet using `json.dump()` that writes dictionary `profile = {'id': 1, 'role': 'admin'}` directly to an open file stream `f`.",
        "starter_code": "import json\nfrom io import StringIO\nprofile = {\"id\": 1, \"role\": \"admin\"}\nf = StringIO()\n# Serialize profile into stream f\n",
        "solution_code": "import json\nfrom io import StringIO\nprofile = {\"id\": 1, \"role\": \"admin\"}\nf = StringIO()\njson.dump(profile, f)\nprint(f.getvalue())",
        "explanation": "`json.dump(obj, f)` streams serialized JSON directly into the writable file stream.",
        "metadata": {"concept": "json_file_stream_dump", "skill": "file_io", "why_this_exercise_exists": "Replaces variation with JSON stream dumping"}
    },
    "14.5_q12": {
        "id": "14.5_q12",
        "type": "output_prediction",
        "concept": "generating_json_loads_parsing",
        "skill": "deserialization",
        "difficulty": "medium",
        "prerequisites": ["14.5_q11"],
        "prompt": "What does `json.loads('{\"active\": true, \"count\": 5}')` return in Python?\n\n```python\nimport json\nparsed = json.loads('{\"active\": true, \"count\": 5}')\nprint(parsed[\"active\"], parsed[\"count\"])\n```",
        "options": [
            "True 5",
            "true 5",
            "\"true\" 5",
            "SyntaxError"
        ],
        "correct_answer": "True 5",
        "explanation": "`json.loads()` converts JSON string primitives back to Python types: JSON `true` becomes Python boolean `True`.",
        "metadata": {"concept": "json_loads_deserialization", "skill": "deserialization", "why_this_exercise_exists": "Replaces variation with JSON string deserialization"}
    },

    # 16.5 Set Comprehensions
    "16.5_q24": {
        "id": "16.5_q24",
        "type": "write_the_code",
        "concept": "set_comprehensions_extension_dedup",
        "skill": "comprehensions",
        "difficulty": "medium",
        "prerequisites": ["16.5_q23"],
        "prompt": "Write a set comprehension to extract the unique file extensions (in lowercase) from `filenames = ['doc.PDF', 'img.png', 'notes.pdf', 'table.csv']`.",
        "starter_code": "filenames = [\"doc.PDF\", \"img.png\", \"notes.pdf\", \"table.csv\"]\n# Build set of unique lowercase extensions\n",
        "solution_code": "filenames = [\"doc.PDF\", \"img.png\", \"notes.pdf\", \"table.csv\"]\nextensions = {f.split(\".\")[-1].lower() for f in filenames}\nprint(sorted(extensions))",
        "explanation": "Set comprehensions `{...}` automatically deduplicate items. Slicing with `.split('.')[-1].lower()` creates `{'csv', 'pdf', 'png'}`.",
        "metadata": {"concept": "set_comprehension_deduplication", "skill": "comprehensions", "why_this_exercise_exists": "Replaces variation with practical set comprehension"}
    },

    # 19.5 Groups and Extraction
    "19.5_q9": {
        "id": "19.5_q9",
        "type": "code_prediction",
        "concept": "regex_non_capturing_groups",
        "skill": "regex",
        "difficulty": "medium",
        "prerequisites": ["19.5_q8"],
        "prompt": "What does the `(?:...)` syntax designate in Python regular expressions?",
        "options": [
            "A non-capturing group that groups tokens for repetition without storing the matched segment in group tuples.",
            "An optional matching group.",
            "A named group with title '?'.",
            "A comment group."
        ],
        "correct_answer": "A non-capturing group that groups tokens for repetition without storing the matched segment in group tuples.",
        "explanation": "Non-capturing groups `(?:...)` allow applying quantifiers like `(?:https?|ftp)` without polluting the `.groups()` tuple or consuming capture index slots.",
        "metadata": {"concept": "non_capturing_groups", "skill": "regex", "why_this_exercise_exists": "Replaces variation with non-capturing regex groups"}
    },
    "19.5_q11": {
        "id": "19.5_q11",
        "type": "output_prediction",
        "concept": "regex_sub_backreferences",
        "skill": "regex_replacement",
        "difficulty": "hard",
        "prerequisites": ["19.5_q10"],
        "prompt": "What does this regex substitution with backreferences produce?\n\n```python\nimport re\ntext = \"John Smith\"\nresult = re.sub(r\"(\\w+)\\s+(\\w+)\", r\"\\2, \\1\", text)\nprint(result)\n```",
        "options": [
            "Smith, John",
            "John, Smith",
            "\\2, \\1",
            "TypeError"
        ],
        "correct_answer": "Smith, John",
        "explanation": "`\\1` refers to capture group 1 (`'John'`) and `\\2` refers to capture group 2 (`'Smith'`). Substituting `r'\\2, \\1'` swaps them to `'Smith, John'`.",
        "metadata": {"concept": "regex_backreference_substitution", "skill": "regex_replacement", "why_this_exercise_exists": "Replaces variation with regex backreference substitution"}
    },

    # 42.2 Data Pipeline (q6)
    "42.2_q6": {
        "id": "42.2_q6",
        "type": "code_ordering",
        "concept": "data_pipeline_lifecycle_ordering",
        "skill": "pipeline_architecture",
        "difficulty": "medium",
        "prerequisites": ["42.2_q5"],
        "prompt": "Arrange the core lifecycle stages of a robust data pipeline in proper execution order:",
        "options": [
            "Ingest raw CSV records from sources",
            "Validate schema and required columns",
            "Clean data, cast types, and impute null values",
            "Merge datasets on key identifiers",
            "Compute analytical metrics and export to disk"
        ],
        "correct_answer": [
            "Ingest raw CSV records from sources",
            "Validate schema and required columns",
            "Clean data, cast types, and impute null values",
            "Merge datasets on key identifiers",
            "Compute analytical metrics and export to disk"
        ],
        "explanation": "A data pipeline follows strict chronological stages: Ingestion -> Schema Validation -> Cleaning/Imputation -> Relational Merging -> Analytical Aggregation/Export.",
        "metadata": {"concept": "data_pipeline_stages", "skill": "pipeline_architecture", "why_this_exercise_exists": "Replaces variation with data pipeline sequence"}
    }
}

