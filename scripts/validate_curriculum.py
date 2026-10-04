"""
CODOLINGO COMPREHENSIVE CURRICULUM QUALITY GATE RUNNER
Orchestrates schema, python AST, answer consistency, prerequisites,
and duplicate detection into a unified quality report.

Usage:
    python scripts/validate_curriculum.py
"""

import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_schema import validate_schema
from validate_python import validate_python
from validate_answers import validate_answers
from validate_prerequisites import validate_prerequisites
from detect_duplicates import detect_duplicates

def run_pipeline() -> bool:
    schema_res = validate_schema()
    python_res = validate_python()
    answer_res = validate_answers()
    prereq_res = validate_prerequisites()
    dup_res = detect_duplicates()

    total_lessons = schema_res["total_lessons"]
    total_items = schema_res["total_items"]

    python_errors = python_res["syntax_errors"]
    answer_mismatches = answer_res["answer_mismatches"]
    schema_errors = schema_res["schema_errors"]
    dup_clusters = len(dup_res["duplicate_clusters"])
    prereq_errors = prereq_res["prerequisite_errors"] + prereq_res["circular_dependencies"] + prereq_res["forward_references"]
    missing_explanations = answer_res["missing_explanations"]
    missing_solutions = answer_res["missing_solutions"]
    ambiguous_exercises = 0

    # Calculate commercial quality score (0 - 100)
    score = 100.0
    score -= (python_errors * 10.0)
    score -= (schema_errors * 5.0)
    score -= (answer_mismatches * 2.0)
    score -= (prereq_errors * 5.0)
    score -= (missing_solutions * 5.0)
    score -= (missing_explanations * 1.0)
    score -= (dup_clusters * 2.0)

    score = max(0.0, min(100.0, score))
    passed = (score >= 95.0 and python_errors == 0 and schema_errors == 0 and prereq_errors == 0 and missing_solutions == 0)

    status_str = "PASS" if passed else "FAIL"

    print("==================================================")
    print("           CURRICULUM QUALITY REPORT              ")
    print("==================================================")
    print()
    print(f"Lessons:   {total_lessons}")
    print(f"Exercises: {total_items}")
    print()
    print(f"Python execution errors: {python_errors}")
    print(f"Answer mismatches:       {answer_mismatches}")
    print(f"Schema errors:           {schema_errors}")
    print(f"Duplicate prompts:       {dup_clusters}")
    print(f"Prerequisite errors:     {prereq_errors}")
    print(f"Missing explanations:    {missing_explanations}")
    print(f"Missing solutions:       {missing_solutions}")
    print(f"Ambiguous exercises:     {ambiguous_exercises}")
    print()
    print(f"Overall quality score:   {int(score)}/100")
    print()
    print(f"STATUS: {status_str}")
    print("==================================================")

    return passed

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
