"""
Unit tests for CurriculumValidator and schema rules.
"""

from pathlib import Path
from generator.validator import CurriculumValidator

def test_benchmark_lesson_validates_cleanly():
    validator = CurriculumValidator()
    benchmark_path = Path("python_content/unit_01/1.2_how_python_works.json")
    result = validator.validate_file(benchmark_path)
    assert result.valid is True
    assert len(result.errors) == 0

def test_missing_top_level_key_detected():
    validator = CurriculumValidator()
    bad_lesson = {
        "lesson_id": "99.1",
        "title": "Bad Lesson",
        # missing "unit" and "items"
    }
    result = validator.validate_lesson_dict(bad_lesson)
    assert result.valid is False
    assert any("unit" in e for e in result.errors)
    assert any("items" in e for e in result.errors)

def test_code_ordering_element_mismatch_detected():
    validator = CurriculumValidator()
    lesson = {
        "lesson_id": "99.2",
        "title": "Ordering Test",
        "unit": "Test Unit",
        "items": [
            {
                "id": "99.2_q1",
                "type": "code_ordering",
                "concept": "testing",
                "skill": "application",
                "difficulty": "easy",
                "prerequisites": [],
                "prompt": "Order the steps",
                "options": ["Step A", "Step B"],
                "correct_answer": ["Step A", "Step C"],  # Step C not in options!
                "explanation": "Test explanation"
            }
        ]
    }
    result = validator.validate_lesson_dict(lesson)
    assert result.valid is False
    assert any("code_ordering" in e for e in result.errors)
