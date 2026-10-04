import json
import glob
from pathlib import Path

files_to_check = [
    "python_content/unit_02/2.1_variables.json",
    "python_content/unit_04/4.3_identity_operators_is_is_not.json",
    "python_content/unit_08/8.3_modifying_lists.json",
    "python_content/unit_08/8.4_list_methods.json",
    "python_content/unit_12/12.3_returning_values.json",
    "python_content/unit_13/13.1_default_arguments.json",
    "python_content/unit_21/21.6_composition.json",
    "python_content/unit_26/26.6_parameterized_queries_and_security.json",
    "python_content/unit_28/28.1_synchronous_vs_asynchronous_execution.json",
    "python_content/unit_33/33.3_sets_for_fast_lookups.json",
]

for pattern in files_to_check:
    matches = glob.glob(pattern)
    if not matches:
        # try fuzzy search
        prefix = pattern.split("/")[-1].split("_")[0]
        unit = pattern.split("/")[1]
        matches = glob.glob(f"python_content/{unit}/{prefix}_*.json")
    for fp in matches:
        print(f"\n=== {fp} ===")
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        print(f"Lesson title: {d.get('title')}")
        for item in d.get("items", [])[:8]:
            title_q = item.get("question") or item.get("prompt") or item.get("title")
            print(f"  [{item.get('id')}] ({item.get('type')}, {item.get('difficulty')}) {title_q[:70] if title_q else 'None'}")
