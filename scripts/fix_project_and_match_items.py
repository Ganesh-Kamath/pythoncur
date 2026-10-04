"""
Replaces remaining duplicate project items (5.6, 42.1, 42.3 items 10, 11, 12)
and makes matching prompts topic-specific across 11.3, 20.5, 28.3.
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
    return False

def run_fixes():
    # 1. Topic-specific match prompts
    def fix_11_3_5(it):
        it["prompt"] = "Match each Python function parameter concept to its correct definition."
    update_item(11, "11.3_parameters_and_arguments.json", "11.3_q5", fix_11_3_5)

    def fix_20_5_5(it):
        it["prompt"] = "Match each OOP instance method term to its appropriate role."
    update_item(20, "20.5_instance_methods.json", "20.5_q5", fix_20_5_5)

    def fix_28_3_5(it):
        it["prompt"] = "Match each concurrent programming concept to its operational behavior."
    update_item(28, "28.3_multiprocessing_concepts.json", "28.3_q5", fix_28_3_5)

    # 2. Project 5.6 Interactive Calculator items 10, 11, 12
    def fix_5_6_10(it):
        it["prompt"] = "In the Interactive Calculator project, implement exponential power calculation using the `**` operator:"
        it["starter_code"] = "def power(base, exponent):\n    return base ___ exponent"
        it["solution_code"] = "def power(base, exponent):\n    return base ** exponent"
        it["explanation"] = "Python uses the double asterisk `**` for exponentiation."
    update_item(5, "5.6_project_interactive_calculator.json", "5.6_q10", fix_5_6_10)

    def fix_5_6_11(it):
        it["prompt"] = "In the Interactive Calculator project, format a floating-point calculation result to exactly 2 decimal places:"
        it["starter_code"] = "def format_result(val):\n    return f'{val:___}'"
        it["solution_code"] = "def format_result(val):\n    return f'{val:.2f}'"
        it["explanation"] = "The format specifier `:.2f` formats floats with 2 fixed decimal digits."
    update_item(5, "5.6_project_interactive_calculator.json", "5.6_q11", fix_5_6_11)

    def fix_5_6_12(it):
        it["prompt"] = "In the Interactive Calculator project, append a completed calculation string to the calculation history list:"
        it["starter_code"] = "history = []\ndef log_calc(record):\n    history.___(record)"
        it["solution_code"] = "history = []\ndef log_calc(record):\n    history.append(record)"
        it["explanation"] = "`history.append(record)` appends the newly computed entry to the end of the history list."
    update_item(5, "5.6_project_interactive_calculator.json", "5.6_q12", fix_5_6_12)

    # 3. Project 42.1 Log Parsing Automation items 10, 11, 12
    def fix_42_1_10(it):
        it["prompt"] = "In the Log Parsing Automation project, extract all IP addresses matching IPv4 format from a raw log line:"
        it["starter_code"] = "import re\ndef extract_ips(line):\n    return re.findall(r'\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b', line)"
        it["solution_code"] = "import re\ndef extract_ips(line):\n    return re.findall(r'\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b', line)"
        it["explanation"] = "Regular expression `\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b` matches IPv4 dotted-decimal octets."
    update_item(42, "42.1_project_log_parsing_automation.json", "42.1_q10", fix_42_1_10)

    def fix_42_1_11(it):
        it["prompt"] = "In the Log Parsing Automation project, sort top 5 IP addresses by visit frequency in descending order:"
        it["starter_code"] = "def top_ips(ip_counts):\n    return sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]"
        it["solution_code"] = "def top_ips(ip_counts):\n    return sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]"
        it["explanation"] = "`reverse=True` orders the key-value frequency pairs from highest count to lowest."
    update_item(42, "42.1_project_log_parsing_automation.json", "42.1_q11", fix_42_1_11)

    def fix_42_1_12(it):
        it["prompt"] = "In the Log Parsing Automation project, write structured log summary statistics to a JSON report file:"
        it["starter_code"] = "import json\ndef save_summary(stats, filepath):\n    with open(filepath, 'w') as f:\n        json.dump(stats, f, indent=2)"
        it["solution_code"] = "import json\ndef save_summary(stats, filepath):\n    with open(filepath, 'w') as f:\n        json.dump(stats, f, indent=2)"
        it["explanation"] = "`json.dump(stats, f, indent=2)` serializes the summary dictionary into formatted JSON on disk."
    update_item(42, "42.1_project_log_parsing_automation.json", "42.1_q12", fix_42_1_12)

    # 4. Project 42.3 Web Scraper items 10, 11, 12
    def fix_42_3_10(it):
        it["prompt"] = "In the Web Scraper API project, clean and normalize relative URLs into absolute URLs using urllib.parse:"
        it["starter_code"] = "from urllib.parse import urljoin\ndef make_absolute(base_url, link):\n    return urljoin(base_url, link)"
        it["solution_code"] = "from urllib.parse import urljoin\ndef make_absolute(base_url, link):\n    return urljoin(base_url, link)"
        it["explanation"] = "`urljoin()` combines a base website URL with relative paths like `/about` safely."
    update_item(42, "42.3_project_interactive_web_scraper_api.json", "42.3_q10", fix_42_3_10)

    def fix_42_3_11(it):
        it["prompt"] = "In the Web Scraper API project, implement a politeness request rate limiter delay between HTTP page fetches:"
        it["starter_code"] = "import time\ndef fetch_with_delay(url, delay_seconds=1.0):\n    time.sleep(delay_seconds)\n    # Proceed to fetch url"
        it["solution_code"] = "import time\ndef fetch_with_delay(url, delay_seconds=1.0):\n    time.sleep(delay_seconds)"
        it["explanation"] = "`time.sleep()` pauses execution to avoid overloading remote web servers during crawling."
    update_item(42, "42.3_project_interactive_web_scraper_api.json", "42.3_q11", fix_42_3_11)

    def fix_42_3_12(it):
        it["prompt"] = "In the Web Scraper API project, save scraped records to a comma-separated values (CSV) file using the csv module:"
        it["starter_code"] = "import csv\ndef export_csv(records, filename):\n    with open(filename, 'w', newline='', encoding='utf-8') as f:\n        writer = csv.DictWriter(f, fieldnames=records[0].keys())\n        writer.writeheader()\n        writer.writerows(records)"
        it["solution_code"] = "import csv\ndef export_csv(records, filename):\n    with open(filename, 'w', newline='', encoding='utf-8') as f:\n        writer = csv.DictWriter(f, fieldnames=records[0].keys())\n        writer.writeheader()\n        writer.writerows(records)"
        it["explanation"] = "`csv.DictWriter` writes dictionary keys as headers and dictionary items as rows."
    update_item(42, "42.3_project_interactive_web_scraper_api.json", "42.3_q12", fix_42_3_12)

if __name__ == "__main__":
    run_fixes()
