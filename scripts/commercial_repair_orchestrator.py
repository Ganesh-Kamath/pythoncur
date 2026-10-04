"""
CODOLINGO MASTER COMMERCIAL REPAIR ORCHESTRATOR
Applies:
1. Explicit question-level replacements for Units 4 to 43
2. Complete purge of calculate_X() templates
3. Elimination of project #13-#18 placeholders
4. Contextual explanation overhaul for all 1,160 generic items
5. Replaces 6.2_q14 with do-while emulation lesson
6. Replaces 42.2_q30 with real data cleaning/merging capstone challenge
7. Comprehensive validation pass
"""

import glob
import json
import os
import shutil
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from curriculum_repairs_units_04_to_14 import REPLACEMENTS_UNITS_04_TO_14
from curriculum_repairs_units_15_to_43 import REPLACEMENTS_UNITS_15_TO_43
from curriculum_repairs_mastery_and_testing import REPLACEMENTS_MASTERY_AND_TESTING
from curriculum_repairs_scaffold_fillers import REPLACEMENTS_SCAFFOLD_FILLERS
from curriculum_repairs_variation_cleanup import REPLACEMENTS_VARIATION_CLEANUP
from curriculum_repairs_microlessons import REPLACEMENTS_MICRO_LESSONS
from curriculum_repairs_explanations import generate_contextual_explanation

WORKSPACE = SCRIPTS_DIR.parent
CONTENT_DIR = WORKSPACE / "python_content"
PYCON_DIR = WORKSPACE / "pycon"

def run_orchestration():
    print("=" * 60)
    print("   CODOLINGO COMMERCIAL-GRADE CURRICULUM REPAIR   ")
    print("=" * 60)

    # 1. Combine all replacements
    staged_replacements = {}
    staged_replacements.update(REPLACEMENTS_UNITS_04_TO_14)
    staged_replacements.update(REPLACEMENTS_UNITS_15_TO_43)
    staged_replacements.update(REPLACEMENTS_MASTERY_AND_TESTING)
    staged_replacements.update(REPLACEMENTS_SCAFFOLD_FILLERS)
    staged_replacements.update(REPLACEMENTS_VARIATION_CLEANUP)
    staged_replacements.update(REPLACEMENTS_MICRO_LESSONS)

    print(f"Loaded {len(staged_replacements)} bespoke pedagogical replacements.")

    files = sorted(glob.glob(str(CONTENT_DIR / "**/*.json"), recursive=True))
    total_inspected = 0
    total_kept = 0
    total_replaced = 0
    generic_explanations_removed = 0
    calculate_templates_removed = 0
    placeholders_removed = 0

    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        lesson_title = data.get("title", "")
        unit_title = data.get("unit", "")
        modified = False

        items = data.get("items", [])
        for i, item in enumerate(items):
            total_inspected += 1
            iid = item.get("id")

            # Check if this item is in our targeted replacements
            if iid in staged_replacements:
                rep = staged_replacements[iid]
                # Preserve prerequisites and idx if needed
                if "prerequisites" not in rep and "prerequisites" in item:
                    rep["prerequisites"] = item["prerequisites"]
                if "idx" in item:
                    rep["idx"] = item["idx"]

                # Track metrics
                if "calculate_" in json.dumps(item):
                    calculate_templates_removed += 1
                if "Project: " in item.get("prompt", "") and any(f"#{num}" in item.get("prompt", "") for num in range(13, 19)):
                    placeholders_removed += 1

                items[i] = rep
                total_replaced += 1
                modified = True
                continue

            # Special case for 24.1_q14 calculate_area -> get_rectangle_area
            if iid == "24.1_q14" and "calculate_area" in json.dumps(item):
                item["prompt"] = "Fill in the blank to create a function that computes rectangle area, following clean naming conventions: def _______(length, width): return length * width"
                item["correct_answer"] = "get_rectangle_area"
                item["accepted_answers"] = ["get_rectangle_area", "compute_area", "rectangle_area"]
                item["explanation"] = "Function names should be descriptive verbs in lowercase with underscores. 'get_rectangle_area' clearly communicates the intent and avoids ambiguity."
                calculate_templates_removed += 1
                modified = True

            # Explanation repair
            expl = item.get("explanation", "")
            if "In Python, this operation directly demonstrates" in expl or len(expl.strip()) < 15:
                new_expl = generate_contextual_explanation(item, lesson_title, unit_title)
                item["explanation"] = new_expl
                generic_explanations_removed += 1
                modified = True

            total_kept += 1

        if modified:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nRepair completed. Verifying residual issues...")

    # Post-check residual issues
    residual_calc = 0
    residual_generic = 0
    residual_proj = 0

    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if "calculate_" in content:
            residual_calc += content.count("calculate_")
        if "In Python, this operation directly demonstrates" in content:
            residual_generic += content.count("In Python, this operation directly demonstrates")
        if "Project: " in content and "#13" in content:
            residual_proj += 1

    print(f"Residual calculate_: {residual_calc}")
    print(f"Residual generic explanations: {residual_generic}")
    print(f"Residual #13 project placeholders: {residual_proj}")

    # Synchronize to pycon
    if PYCON_DIR.exists():
        pycon_content = PYCON_DIR / "python_content"
        if pycon_content.exists():
            shutil.rmtree(pycon_content)
        shutil.copytree(CONTENT_DIR, pycon_content)
        print("Synchronized updated python_content to pycon/ repository.")

    print("\nSummary of modifications:")
    print(f"  Exercises inspected:           {total_inspected}")
    print(f"  Exercises kept:                {total_kept}")
    print(f"  Exercises replaced:            {total_replaced}")
    print(f"  Placeholder exercises removed: {placeholders_removed}")
    print(f"  Generic explanations removed:  {generic_explanations_removed}")
    print(f"  Template exercises removed:    {calculate_templates_removed}")

if __name__ == "__main__":
    run_orchestration()
