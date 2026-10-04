"""
Core Curriculum Generator Engine for Codolingo.
Orchestrates prompt generation, Sarvam API calls, local validation, QA repair, and atomic checkpointing.
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from generator.git_helper import GitHelper
from generator.prompts_loader import PromptsLoader
from generator.sarvam_client import SarvamClient
from generator.state_manager import StateManager
from generator.syllabus_parser import LessonInfo, SyllabusParser, UnitInfo
from generator.validator import CurriculumValidator, ValidationResult

logger = logging.getLogger("CurriculumGenerator")

class CurriculumGenerator:
    def __init__(
        self,
        content_dir: Optional[Path] = None,
        sarvam_client: Optional[SarvamClient] = None,
        validator: Optional[CurriculumValidator] = None,
        state_manager: Optional[StateManager] = None,
        prompts_loader: Optional[PromptsLoader] = None,
        syllabus_parser: Optional[SyllabusParser] = None,
        git_helper: Optional[GitHelper] = None,
        checkpoint_interval: int = 5,
        max_qa_attempts: int = 2,
    ):
        self.content_dir = Path(content_dir or "python_content")
        self.content_dir.mkdir(parents=True, exist_ok=True)

        self.sarvam = sarvam_client or SarvamClient()
        self.validator = validator or CurriculumValidator()
        self.state = state_manager or StateManager()
        self.prompts = prompts_loader or PromptsLoader()
        self.syllabus = syllabus_parser or SyllabusParser()
        self.git = git_helper or GitHelper()

        self.checkpoint_interval = checkpoint_interval
        self.max_qa_attempts = max_qa_attempts
        self.lessons_since_last_checkpoint = 0

    def get_lesson_filepath(self, lesson: LessonInfo) -> Path:
        """Return the destination path for a lesson JSON file."""
        unit_folder = self.content_dir / lesson.unit_id
        unit_folder.mkdir(parents=True, exist_ok=True)
        return unit_folder / lesson.filename

    def generate_single_lesson(self, lesson: LessonInfo, force: bool = False) -> Tuple[bool, str]:
        """
        Generate, validate, repair, and persist a single lesson.
        Returns:
            (success: bool, status_message: str)
        """
        dest_path = self.get_lesson_filepath(lesson)

        # 1. Skip if already completed and valid unless force=True
        if not force and self.state.is_lesson_completed(lesson.lesson_id) and dest_path.exists():
            val_res = self.validator.validate_file(dest_path)
            if val_res.valid:
                msg = f"Lesson {lesson.lesson_id} already exists and passes validation. Skipping."
                print(f"[SKIP] {msg}")
                return True, msg

        print(f"\n[{time.strftime('%H:%M:%S')}] >>> Generating Lesson {lesson.lesson_id}: {lesson.title} ({lesson.unit_title})")
        self.state.set_current_position(lesson.unit_num, lesson.lesson_id)

        # 2. Build Generation Prompt
        prev_lessons = self.syllabus.get_previous_lessons(lesson.lesson_id, limit=3)
        prompt_text = self.prompts.build_generation_prompt(lesson, prev_lessons, target_item_count=30)

        messages = [
            {"role": "system", "content": "You are the Codolingo Python curriculum master engine. Return valid JSON only."},
            {"role": "user", "content": prompt_text}
        ]

        # 3. Call Sarvam API
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Calling Sarvam API ({self.sarvam.model})...")
            raw_response = self.sarvam.complete(messages, temperature=0.2, max_tokens=8192)
            lesson_dict = self.sarvam.extract_json(raw_response)
        except Exception as api_err:
            err_msg = f"API generation failed for {lesson.lesson_id}: {api_err}"
            print(f"[ERROR] {err_msg}")
            self.state.mark_lesson_failed(lesson.lesson_id, str(api_err), attempts=1)
            return False, err_msg

        # Ensure top-level metadata matches syllabus
        lesson_dict["lesson_id"] = lesson.lesson_id
        lesson_dict["title"] = lesson.title
        lesson_dict["unit"] = lesson.unit_title

        # 4. Local Validation
        print(f"[{time.strftime('%H:%M:%S')}] Running local deterministic validation...")
        val_res = self.validator.validate_lesson_dict(lesson_dict)

        # 5. Targeted QA Repair loop if invalid
        qa_attempt = 0
        while not val_res.valid and qa_attempt < self.max_qa_attempts:
            qa_attempt += 1
            print(f"[{time.strftime('%H:%M:%S')}] Validation failed ({len(val_res.errors)} errors). Requesting targeted repair (attempt {qa_attempt}/{self.max_qa_attempts})...")
            for err in val_res.errors[:4]:
                print(f"   [Error to repair] {err}")

            try:
                qa_prompt = self.prompts.build_qa_prompt(
                    lesson_id=lesson.lesson_id,
                    lesson_title=lesson.title,
                    lesson_json_str=json.dumps(lesson_dict, indent=2),
                    errors=val_res.errors
                )
                qa_messages = [
                    {"role": "system", "content": "You are the Codolingo curriculum QA engine. Fix the errors and return corrected JSON only."},
                    {"role": "user", "content": qa_prompt}
                ]
                repaired_raw = self.sarvam.complete(qa_messages, temperature=0.1, max_tokens=8192)
                repaired_dict = self.sarvam.extract_json(repaired_raw)
                repaired_dict["lesson_id"] = lesson.lesson_id
                repaired_dict["title"] = lesson.title
                repaired_dict["unit"] = lesson.unit_title

                val_res = self.validator.validate_lesson_dict(repaired_dict)
                if val_res.valid or len(val_res.errors) < len(val_res.errors):
                    lesson_dict = repaired_dict
            except Exception as qa_err:
                print(f"[QA Warning] Repair request failed: {qa_err}")

        # 6. Check final validation result
        if not val_res.valid:
            err_summary = "; ".join(val_res.errors[:3])
            print(f"[FAILED] Lesson {lesson.lesson_id} could not be validated after {qa_attempt} repair attempts: {err_summary}")
            self.state.mark_lesson_failed(lesson.lesson_id, err_summary, attempts=qa_attempt + 1)
            return False, f"Validation failure: {err_summary}"

        # 7. Persist Valid Lesson
        item_count = len(lesson_dict.get("items", []))
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(lesson_dict, f, indent=2)

        print(f"[{time.strftime('%H:%M:%S')}] [SUCCESS] Saved valid lesson: {dest_path.name} ({item_count} items)")

        # 8. Update State Checkpoint
        self.state.mark_lesson_completed(lesson.lesson_id, item_count=item_count)
        self.lessons_since_last_checkpoint += 1

        # Check if unit completed
        unit_info = self.syllabus.get_unit(lesson.unit_num)
        if unit_info:
            all_unit_ids = [l.lesson_id for l in unit_info.lessons]
            if self.state.update_unit_completion(lesson.unit_num, all_unit_ids):
                print(f"[{time.strftime('%H:%M:%S')}] *** Unit {lesson.unit_num} ({unit_info.title}) 100% COMPLETE! ***")

        # 9. Optional Git Checkpoint
        if self.lessons_since_last_checkpoint >= self.checkpoint_interval:
            self.git.checkpoint(f"checkpoint(curriculum): generate lessons up to {lesson.lesson_id}")
            self.lessons_since_last_checkpoint = 0

        return True, f"Generated and validated {lesson.lesson_id} successfully."

    def generate_all(self, resume: bool = True, force: bool = False) -> None:
        """Generate all lessons in syllabus from 1.1 to 43.5 sequentially."""
        all_lessons = self.syllabus.all_lessons()
        total = len(all_lessons)
        print(f"\n========================================================")
        print(f"  Codolingo Python Curriculum Generation Engine")
        print(f"  Target: {total} lessons (1.1 -> 43.5)")
        print(f"  Model: {self.sarvam.model}")
        print(f"  Resume Mode: {resume}")
        print(f"========================================================\n")

        successful = 0
        skipped = 0
        failed = 0

        for idx, lesson in enumerate(all_lessons, start=1):
            if resume and not force and self.state.is_lesson_completed(lesson.lesson_id):
                dest_path = self.get_lesson_filepath(lesson)
                if dest_path.exists():
                    print(f"[{idx}/{total}] Lesson {lesson.lesson_id} already complete. [SKIP]")
                    skipped += 1
                    continue

            print(f"\n[{idx}/{total}] Processing Lesson {lesson.lesson_id} of {total}...")
            ok, msg = self.generate_single_lesson(lesson, force=force)
            if ok:
                successful += 1
            else:
                failed += 1

        print(f"\n========================================================")
        print(f"  Generation Run Finished")
        print(f"  Total Processed: {total}")
        print(f"  Newly Succeeded: {successful}")
        print(f"  Skipped (Existing): {skipped}")
        print(f"  Failed Lessons: {failed}")
        if self.state.state.get("failed_lessons"):
            print("  Failed lesson IDs:")
            for flid, finfo in self.state.state["failed_lessons"].items():
                print(f"    - {flid}: {finfo.get('error')}")
        print(f"========================================================\n")

    def generate_unit(self, unit_num: int, force: bool = False) -> None:
        """Generate all lessons for a specific unit number (e.g. 1)."""
        unit = self.syllabus.get_unit(unit_num)
        if not unit:
            print(f"[ERROR] Unit {unit_num} not found in syllabus.")
            return

        print(f"\nGenerating all lessons for Unit {unit_num}: {unit.title} ({len(unit.lessons)} lessons)")
        for l in unit.lessons:
            self.generate_single_lesson(l, force=force)

    def generate_specific_lesson(self, lesson_id: str, force: bool = False) -> bool:
        """Generate a single target lesson by its ID (e.g. '1.3')."""
        lesson = self.syllabus.get_lesson(lesson_id)
        if not lesson:
            print(f"[ERROR] Lesson ID '{lesson_id}' not found in syllabus.")
            return False

        ok, msg = self.generate_single_lesson(lesson, force=force)
        return ok
