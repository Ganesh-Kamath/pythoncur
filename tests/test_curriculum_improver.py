import json
import pytest
from pathlib import Path
import tempfile
import shutil

from curriculum_improver.health_tracker import HealthTracker
from curriculum_improver.quality_gate import QualityGate
from curriculum_improver.version_manager import VersionManager
from curriculum_improver.queue_manager import QueueManager
from curriculum_improver.sarvam_reviewer import ReviewResult


@pytest.fixture
def sample_lesson():
    return {
        "lesson_id": "1.1",
        "title": "Introduction to Python",
        "unit": "Python Foundations",
        "items": [
            {
                "id": "1.1_q1",
                "type": "micro_lesson",
                "concept": "syntax",
                "skill": "recognition",
                "difficulty": "easy",
                "prerequisites": [],
                "title": "Welcome",
                "content": "Python is an easy to read programming language.",
            },
            {
                "id": "1.1_q2",
                "type": "multiple_choice",
                "concept": "syntax",
                "skill": "recall",
                "difficulty": "easy",
                "prerequisites": ["1.1_q1"],
                "prompt": "What extension do Python files use?",
                "options": [".py", ".python", ".pt", ".pyth"],
                "correct_answer": ".py",
                "explanation": "Python source files conventionally use the .py file extension.",
            },
            {
                "id": "1.1_q3",
                "type": "write_the_code",
                "concept": "printing",
                "skill": "application",
                "difficulty": "medium",
                "prerequisites": ["1.1_q2"],
                "prompt": "Write code to print 42",
                "starter_code": "",
                "solution_code": "print(42)",
                "test_cases": [{"input": "", "expected_output": "42"}],
                "explanation": "Use print(42) to output numbers.",
            }
        ]
    }


def test_health_tracker_evaluation(sample_lesson):
    tracker = HealthTracker()
    report = tracker.evaluate_lesson(sample_lesson)
    assert report.lesson_id == "1.1"
    assert 0 <= report.overall_health <= 100
    assert report.correctness >= 90
    assert report.concept_coverage > 0
    # Telemetry is unavailable so learner metrics must be clearly flagged
    assert report.learner_data_status == "unavailable"


def test_quality_gate_mcq_validation():
    gate = QualityGate()
    # Valid MCQ
    valid_mcq = {
        "id": "test_mcq",
        "type": "multiple_choice",
        "concept": "functions",
        "skill": "recognition",
        "difficulty": "easy",
        "prompt": "Which keyword defines a function?",
        "options": ["def", "func", "function", "lambda"],
        "correct_answer": "def",
        "explanation": "In Python, the def keyword defines functions.",
    }
    res = gate.validate_item(valid_mcq)
    assert res.passed is True
    assert len(res.errors) == 0

    # Invalid MCQ: correct answer not in options
    invalid_mcq = dict(valid_mcq, correct_answer="define")
    res_bad = gate.validate_item(invalid_mcq)
    assert res_bad.passed is False
    assert any("not present in options" in e for e in res_bad.errors)


def test_quality_gate_python_code_execution():
    gate = QualityGate()
    # Valid code
    valid_code = {
        "id": "test_code",
        "type": "write_the_code",
        "concept": "output",
        "skill": "application",
        "difficulty": "easy",
        "prompt": "Print 'Hello'",
        "solution_code": "print('Hello')",
        "test_cases": [{"input": "", "expected_output": "Hello"}],
    }
    res = gate.validate_item(valid_code, execute_code=True)
    assert res.passed is True

    # Syntax error code
    bad_syntax = dict(valid_code, solution_code="print('Hello'")
    res_syntax = gate.validate_item(bad_syntax, execute_code=True)
    assert res_syntax.passed is False
    assert any("SyntaxError" in e for e in res_syntax.errors)


def test_version_manager_lifecycle(sample_lesson):
    vm = VersionManager()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        active_file = temp_path / "1.1_test.json"
        with open(active_file, "w", encoding="utf-8") as f:
            json.dump(sample_lesson, f, indent=2)

        # Baseline snapshot
        v1_path = vm.ensure_initial_version("99.1", active_file)
        assert v1_path.exists()
        assert "v001.json" in str(v1_path)

        # Commit an accepted change
        mod_lesson = dict(sample_lesson)
        mod_lesson["items"][1]["explanation"] = "Updated explanation."
        v2_path = vm.commit_accepted_change(
            lesson_id="99.1",
            active_filepath=active_file,
            new_lesson_dict=mod_lesson,
            question_id="1.1_q2",
            reason="Clarified extension rationale",
            evidence="Pedagogical audit",
            model_used="qwen3:8b",
            validation_passed=True,
            sarvam_review={"decision": "accept", "reasoning_summary": "Solid"},
            score_before=80,
            score_after=88
        )
        assert v2_path.exists()
        assert "v002.json" in str(v2_path)

        # Clean up temporary test lesson version folder
        test_vdir = vm._get_lesson_versions_dir("99.1")
        if test_vdir.exists():
            shutil.rmtree(test_vdir)


def test_queue_manager_prioritization():
    db_path = Path("data/test_temp_queue.db")
    if db_path.exists():
        db_path.unlink()

    try:
        qm = QueueManager(db_path=db_path)

        qm.enqueue(task_type="audit", priority=50, lesson_id="1.1", reason="Routine", evidence="Schedule")
        qm.enqueue(task_type="fix_high_failure", priority=90, lesson_id="1.2", reason="78% failure rate", evidence="Telemetry")
        qm.enqueue(task_type="improve_explanation", priority=30, lesson_id="1.3", reason="Low priority", evidence="Audit")

        assert qm.get_queue_counts()["total"] == 3

        # Should pop highest priority first (priority 90 for lesson 1.2)
        popped = qm.pop_highest_priority_task()
        assert popped is not None
        assert popped.lesson_id == "1.2"
        assert popped.priority == 90

        qm.mark_completed(popped.task_id)
        assert qm.get_queue_counts()["total"] == 2
    finally:
        if db_path.exists():
            try:
                db_path.unlink()
            except Exception:
                pass


def test_review_result_acceptance_criteria():
    good_review = ReviewResult(
        decision="accept",
        conceptual_correctness=95,
        pedagogical_quality=85,
        difficulty_quality=90,
        clarity=90,
        ambiguity=10,
        exercise_alignment=95,
        reasoning_summary="Excellent improvement"
    )
    assert good_review.is_accepted() is True

    # Ambiguous review should be rejected
    ambiguous_review = ReviewResult(
        decision="accept",
        conceptual_correctness=95,
        pedagogical_quality=85,
        difficulty_quality=90,
        clarity=90,
        ambiguity=40,  # Too ambiguous (>25)
        exercise_alignment=95,
        reasoning_summary="Ambiguous distractor"
    )
    assert ambiguous_review.is_accepted() is False

    # Low correctness review should be rejected
    low_correctness = ReviewResult(
        decision="accept",
        conceptual_correctness=70,  # Below 85
        pedagogical_quality=85,
        difficulty_quality=90,
        clarity=90,
        ambiguity=10,
        exercise_alignment=95,
        reasoning_summary="Factual inaccuracy"
    )
    assert low_correctness.is_accepted() is False
