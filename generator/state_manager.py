"""
State Manager for Codolingo Curriculum Generator.
Provides persistent, atomic tracking of generation progress across sessions.
"""

import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

DEFAULT_STATE_FILE = Path("generation_state.json")

class StateManager:
    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = Path(state_file or DEFAULT_STATE_FILE)
        self.state: Dict[str, Any] = {
            "curriculum_version": "1.0.0",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "current_unit": 1,
            "current_lesson": "1.1",
            "units_completed": [],
            "lessons_completed": [],
            "failed_lessons": {},
            "validation_status": {},
            "stats": {
                "total_units": 43,
                "total_lessons_target": 234,
                "completed_lessons": 0,
                "failed_count": 0,
                "total_items": 0,
            }
        }
        self.load()

    def load(self) -> None:
        """Load state from disk if it exists."""
        if not self.state_file.exists():
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                # Merge loaded state with defaults
                for key, val in loaded.items():
                    if key == "stats" and isinstance(val, dict):
                        self.state["stats"].update(val)
                    else:
                        self.state[key] = val
        except Exception as e:
            print(f"[StateManager] Warning: Could not load state file ({e}). Starting with clean state.")

    def save(self) -> None:
        """Atomically save state to disk using a temporary file."""
        self.state["last_updated"] = datetime.now(timezone.utc).isoformat()
        self.state["stats"]["completed_lessons"] = len(self.state.get("lessons_completed", []))
        self.state["stats"]["failed_count"] = len(self.state.get("failed_lessons", {}))

        # Atomic write
        temp_dir = self.state_file.parent if self.state_file.parent.exists() else Path(".")
        with tempfile.NamedTemporaryFile("w", dir=temp_dir, delete=False, encoding="utf-8") as tf:
            json.dump(self.state, tf, indent=2)
            temp_name = tf.name

        shutil.move(temp_name, self.state_file)

    def is_lesson_completed(self, lesson_id: str) -> bool:
        """Check if a lesson is already recorded as successfully completed."""
        return lesson_id in self.state.get("lessons_completed", [])

    def mark_lesson_completed(self, lesson_id: str, item_count: int = 30) -> None:
        """Mark a lesson as successfully completed and validated."""
        completed: List[str] = self.state.setdefault("lessons_completed", [])
        if lesson_id not in completed:
            completed.append(lesson_id)

        # Remove from failed if previously recorded
        failed: Dict[str, Any] = self.state.setdefault("failed_lessons", {})
        if lesson_id in failed:
            del failed[lesson_id]

        self.state.setdefault("validation_status", {})[lesson_id] = "VALID"
        self.state["stats"]["total_items"] = self.state["stats"].get("total_items", 0) + item_count
        self.save()

    def mark_lesson_failed(self, lesson_id: str, error_message: str, attempts: int) -> None:
        """Record a lesson failure with error details without stopping the process."""
        failed = self.state.setdefault("failed_lessons", {})
        failed[lesson_id] = {
            "error": error_message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "attempts": attempts,
        }
        self.state.setdefault("validation_status", {})[lesson_id] = "FAILED"
        self.save()

    def set_current_position(self, unit_num: int, lesson_id: str) -> None:
        """Update current active processing pointer."""
        self.state["current_unit"] = unit_num
        self.state["current_lesson"] = lesson_id
        self.save()

    def update_unit_completion(self, unit_num: int, all_unit_lessons: List[str]) -> bool:
        """Check if all lessons in a unit are complete, and mark the unit completed if so."""
        completed_set = set(self.state.get("lessons_completed", []))
        if all(lid in completed_set for lid in all_unit_lessons):
            units_completed = self.state.setdefault("units_completed", [])
            if unit_num not in units_completed:
                units_completed.append(unit_num)
                units_completed.sort()
            self.save()
            return True
        return False

    def sync_with_filesystem(self, content_dir: Path) -> int:
        """Scan content directory to discover and register all valid existing lessons."""
        if not content_dir.exists():
            return 0

        synced_count = 0
        total_items = 0
        completed = set(self.state.get("lessons_completed", []))

        for json_file in content_dir.glob("unit_*/*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                lesson_id = data.get("lesson_id")
                items = data.get("items", [])
                if lesson_id and len(items) >= 20:
                    completed.add(lesson_id)
                    total_items += len(items)
                    synced_count += 1
            except Exception:
                continue

        self.state["lessons_completed"] = sorted(list(completed), key=lambda x: [int(p) if p.isdigit() else p for p in x.split(".")])
        self.state["stats"]["completed_lessons"] = len(self.state["lessons_completed"])
        self.state["stats"]["total_items"] = total_items
        self.save()
        return synced_count
