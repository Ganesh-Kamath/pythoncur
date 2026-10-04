"""
Unit tests for StateManager persistence and atomic operations.
"""

import tempfile
from pathlib import Path
from generator.state_manager import StateManager

def test_state_manager_persistence():
    with tempfile.TemporaryDirectory() as td:
        sf = Path(td) / "test_state.json"
        sm = StateManager(state_file=sf)
        assert sm.is_lesson_completed("1.1") is False

        sm.mark_lesson_completed("1.1", item_count=30)
        assert sm.is_lesson_completed("1.1") is True

        # Reload from disk
        sm2 = StateManager(state_file=sf)
        assert sm2.is_lesson_completed("1.1") is True
        assert sm2.state["stats"]["completed_lessons"] == 1
        assert sm2.state["stats"]["total_items"] == 30

def test_state_manager_failed_tracking():
    with tempfile.TemporaryDirectory() as td:
        sf = Path(td) / "test_state.json"
        sm = StateManager(state_file=sf)
        sm.mark_lesson_failed("8.4", "Rate limited 429", attempts=4)

        assert "8.4" in sm.state["failed_lessons"]
        assert sm.state["failed_lessons"]["8.4"]["attempts"] == 4

        # Marking completed clears it from failed
        sm.mark_lesson_completed("8.4", item_count=30)
        assert "8.4" not in sm.state["failed_lessons"]
        assert sm.is_lesson_completed("8.4") is True
