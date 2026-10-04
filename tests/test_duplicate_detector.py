"""
Unit tests for DuplicateDetector.
"""

from generator.duplicate_detector import DuplicateDetector

def test_exact_duplicate_prompt_detected():
    detector = DuplicateDetector()
    items = [
        {
            "id": "1.1_q1",
            "type": "multiple_choice",
            "prompt": "What does a CPU do inside a modern computer?",
        },
        {
            "id": "1.1_q2",
            "type": "multiple_choice",
            "prompt": "What does a CPU do inside a modern computer?",
        }
    ]
    errors, warnings = detector.check_lesson_items(items)
    assert len(errors) >= 1
    assert any("Exact duplicate" in e for e in errors)

def test_normalized_duplicate_prompt_detected():
    detector = DuplicateDetector()
    items = [
        {
            "id": "1.1_q1",
            "type": "multiple_choice",
            "prompt": "What does a CPU do inside a computer?",
        },
        {
            "id": "1.1_q2",
            "type": "multiple_choice",
            "prompt": "What does a CPU do, inside a computer??",
        }
    ]
    errors, warnings = detector.check_lesson_items(items)
    assert len(errors) >= 1
    assert any("duplicate prompt" in e.lower() for e in errors)
