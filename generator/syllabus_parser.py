"""
Syllabus Parser for Codolingo Master Curriculum.
Parses PYTHON_MASTER_SYLLABUS.txt into structured Unit and Lesson objects.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

@dataclass
class LessonInfo:
    lesson_id: str          # e.g. "1.1"
    unit_num: int           # e.g. 1
    unit_id: str            # e.g. "unit_01"
    unit_title: str         # e.g. "Python Foundations"
    title: str              # e.g. "What Is Programming?"
    slug: str               # e.g. "what_is_programming"
    filename: str           # e.g. "1.1_what_is_programming.json"
    is_project: bool        # e.g. True if "Project:" in title

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lesson_id": self.lesson_id,
            "unit_num": self.unit_num,
            "unit_id": self.unit_id,
            "unit_title": self.unit_title,
            "title": self.title,
            "slug": self.slug,
            "filename": self.filename,
            "is_project": self.is_project,
        }

@dataclass
class UnitInfo:
    unit_num: int
    unit_id: str            # "unit_01"
    title: str
    lessons: List[LessonInfo] = field(default_factory=list)

class SyllabusParser:
    def __init__(self, syllabus_path: Optional[Path] = None):
        self.syllabus_path = Path(syllabus_path or "PYTHON_MASTER_SYLLABUS.txt")
        self.units: List[UnitInfo] = []
        self.lessons_by_id: Dict[str, LessonInfo] = {}
        self.parse()

    @staticmethod
    def slugify(text: str) -> str:
        """Convert a title to a clean snake_case filename slug."""
        text = text.lower()
        # Remove parenthesized phrases or special characters
        text = re.sub(r"\(.*?\)", "", text)
        text = re.sub(r"project:\s*", "project_", text)
        text = re.sub(r"[^a-z0-9]+", "_", text)
        return text.strip("_")

    def parse(self) -> None:
        """Parse the syllabus text file into units and lessons."""
        if not self.syllabus_path.exists():
            raise FileNotFoundError(f"Syllabus file not found: {self.syllabus_path}")

        current_unit: Optional[UnitInfo] = None
        unit_pattern = re.compile(r"^(\d+)\.\s+(.*)$")
        lesson_pattern = re.compile(r"^\s*(\d+\.\d+)\s+(.*)$")

        with open(self.syllabus_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.rstrip()
                if not line:
                    continue

                # Check for unit header: e.g. "1. Python Foundations"
                unit_match = unit_pattern.match(line)
                if unit_match and not line.startswith("   ") and not line.startswith("\t"):
                    unit_num = int(unit_match.group(1))
                    unit_title = unit_match.group(2).strip()
                    unit_id = f"unit_{unit_num:02d}"
                    current_unit = UnitInfo(unit_num=unit_num, unit_id=unit_id, title=unit_title)
                    self.units.append(current_unit)
                    continue

                # Check for lesson: e.g. "   1.1 What Is Programming?"
                lesson_match = lesson_pattern.match(line)
                if lesson_match and current_unit:
                    lid = lesson_match.group(1).strip()
                    title = lesson_match.group(2).strip()
                    slug = self.slugify(title)
                    filename = f"{lid}_{slug}.json"
                    is_project = "project:" in title.lower()

                    lesson = LessonInfo(
                        lesson_id=lid,
                        unit_num=current_unit.unit_num,
                        unit_id=current_unit.unit_id,
                        unit_title=current_unit.title,
                        title=title,
                        slug=slug,
                        filename=filename,
                        is_project=is_project,
                    )
                    current_unit.lessons.append(lesson)
                    self.lessons_by_id[lid] = lesson

    def get_lesson(self, lesson_id: str) -> Optional[LessonInfo]:
        """Retrieve lesson metadata by its ID (e.g. '1.3')."""
        return self.lessons_by_id.get(lesson_id)

    def get_unit(self, unit_num: int) -> Optional[UnitInfo]:
        """Retrieve unit metadata by number (1-43)."""
        for u in self.units:
            if u.unit_num == unit_num:
                return u
        return None

    def all_lessons(self) -> List[LessonInfo]:
        """Return all lessons across the entire curriculum in order."""
        ordered = []
        for u in self.units:
            ordered.extend(u.lessons)
        return ordered

    def get_previous_lessons(self, lesson_id: str, limit: int = 3) -> List[LessonInfo]:
        """Get immediate preceding lessons for contextual prerequisite chaining."""
        all_l = self.all_lessons()
        idx = next((i for i, l in enumerate(all_l) if l.lesson_id == lesson_id), -1)
        if idx <= 0:
            return []
        start = max(0, idx - limit)
        return all_l[start:idx]
