"""
Prompts Loader for Codolingo Curriculum Generator.
Loads prompt templates from disk and formats them with lesson context and quality benchmarks.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from generator.syllabus_parser import LessonInfo, SyllabusParser

DEFAULT_PROMPTS_DIR = Path("prompts")
DEFAULT_BENCHMARK_PATH = Path("python_content/unit_01/1.2_how_python_works.json")

class PromptsLoader:
    def __init__(self, prompts_dir: Optional[Path] = None, benchmark_path: Optional[Path] = None):
        self.prompts_dir = Path(prompts_dir or DEFAULT_PROMPTS_DIR)
        self.benchmark_path = Path(benchmark_path or DEFAULT_BENCHMARK_PATH)
        self._master_prompt: Optional[str] = None
        self._generation_template: Optional[str] = None
        self._qa_template: Optional[str] = None
        self._benchmark_excerpt: Optional[str] = None

    def get_master_prompt(self) -> str:
        if self._master_prompt is None:
            path = self.prompts_dir / "master_curriculum_prompt.txt"
            with open(path, "r", encoding="utf-8") as f:
                self._master_prompt = f.read()
        return self._master_prompt

    def get_generation_template(self) -> str:
        if self._generation_template is None:
            path = self.prompts_dir / "lesson_generation_prompt.txt"
            with open(path, "r", encoding="utf-8") as f:
                self._generation_template = f.read()
        return self._generation_template

    def get_qa_template(self) -> str:
        if self._qa_template is None:
            path = self.prompts_dir / "lesson_qa_prompt.txt"
            with open(path, "r", encoding="utf-8") as f:
                self._qa_template = f.read()
        return self._qa_template

    def get_benchmark_excerpt(self) -> str:
        """Extract a high quality 5-item representative sample from Lesson 1.2."""
        if self._benchmark_excerpt is None:
            if not self.benchmark_path.exists():
                return "{}"
            try:
                with open(self.benchmark_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                items = data.get("items", [])
                # Take sample of varied items: micro_lesson (q1), multiple_choice (q2), match (q4), ordering (q7), fill_in_blank (q23)
                sample_ids = {"1.2_q1", "1.2_q2", "1.2_q4", "1.2_q7", "1.2_q23"}
                sample_items = [it for it in items if it.get("id") in sample_ids]
                if not sample_items:
                    sample_items = items[:5]
                sample_dict = {
                    "lesson_id": "1.2",
                    "title": "How Python Works",
                    "unit": "Python Foundations",
                    "items": sample_items
                }
                self._benchmark_excerpt = json.dumps(sample_dict, indent=2)
            except Exception:
                self._benchmark_excerpt = "{}"
        return self._benchmark_excerpt

    def build_generation_prompt(
        self,
        lesson: LessonInfo,
        previous_lessons: List[LessonInfo],
        target_item_count: int = 30
    ) -> str:
        """Construct the prompt sent to Sarvam for generating a new lesson."""
        master = self.get_master_prompt()
        template = self.get_generation_template()
        benchmark = self.get_benchmark_excerpt()

        if previous_lessons:
            prereq_lines = [f"- Lesson {pl.lesson_id}: {pl.title} (Unit {pl.unit_num})" for pl in previous_lessons]
            prereq_summary = "Learners have previously completed the following foundational lessons:\n" + "\n".join(prereq_lines)
        else:
            prereq_summary = "This is the very first lesson or has no immediate prerequisites."

        syllabus_pos = f"Unit {lesson.unit_num} ({lesson.unit_title}) - Lesson {lesson.lesson_id} ({lesson.title})"

        prompt = template.format(
            master_rules=master,
            unit_id=lesson.unit_id,
            unit_name=lesson.unit_title,
            lesson_id=lesson.lesson_id,
            lesson_title=lesson.title,
            syllabus_position=syllabus_pos,
            prerequisite_summary=prereq_summary,
            benchmark_example=benchmark,
            target_item_count=target_item_count,
        )
        return prompt

    def build_qa_prompt(self, lesson_id: str, lesson_title: str, lesson_json_str: str, errors: List[str]) -> str:
        """Construct the prompt sent to Sarvam for targeted QA repair."""
        template = self.get_qa_template()
        err_str = "\n".join(f"- {err}" for err in errors)
        return template.format(
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            validation_errors=err_str,
            lesson_json=lesson_json_str,
        )
