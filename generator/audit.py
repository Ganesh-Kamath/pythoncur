"""
Curriculum Audit Engine for Codolingo Python Curriculum.
Conducts full system audit, validates all lessons, verifies syllabus coverage, and generates audit reports.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from generator.syllabus_parser import LessonInfo, SyllabusParser
from generator.validator import CurriculumValidator, ValidationResult

class CurriculumAuditor:
    def __init__(self, content_dir: Optional[Path] = None, syllabus_parser: Optional[SyllabusParser] = None):
        self.content_dir = Path(content_dir or "python_content")
        self.syllabus = syllabus_parser or SyllabusParser()
        self.validator = CurriculumValidator()

    def run_audit(self, json_output: str = "curriculum_audit.json", txt_output: str = "curriculum_audit.txt") -> Dict[str, Any]:
        """Run full curriculum audit against all syllabus lessons and write reports."""
        all_lessons = self.syllabus.all_lessons()
        total_target_lessons = len(all_lessons)

        missing_lessons: List[str] = []
        valid_lessons: List[str] = []
        invalid_lessons: Dict[str, List[str]] = {}
        lessons_with_warnings: Dict[str, List[str]] = {}

        total_items = 0
        type_counts: Dict[str, int] = {}
        difficulty_counts: Dict[str, int] = {}
        all_seen_item_ids: Set[str] = set()
        duplicate_global_ids: List[str] = []

        project_lessons_audited: Dict[str, bool] = {}
        dsa_lessons_audited: Dict[str, bool] = {}

        for lesson in all_lessons:
            # Expected file in python_content/unit_XX/
            unit_dir = self.content_dir / lesson.unit_id
            target_file = None
            if unit_dir.exists():
                candidates = list(unit_dir.glob(f"{lesson.lesson_id}_*.json"))
                if candidates:
                    target_file = candidates[0]

            if not target_file or not target_file.exists():
                missing_lessons.append(lesson.lesson_id)
                continue

            res = self.validator.validate_file(target_file)
            if not res.valid:
                invalid_lessons[lesson.lesson_id] = res.errors
            else:
                valid_lessons.append(lesson.lesson_id)

            if res.warnings:
                lessons_with_warnings[lesson.lesson_id] = res.warnings

            # Item details
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    ldata = json.load(f)
                items = ldata.get("items", [])
                total_items += len(items)

                has_coding_item = False
                for it in items:
                    iid = it.get("id")
                    if iid in all_seen_item_ids:
                        duplicate_global_ids.append(iid)
                    all_seen_item_ids.add(iid)

                    itype = it.get("type", "unknown")
                    type_counts[itype] = type_counts.get(itype, 0) + 1

                    diff = it.get("difficulty", "medium")
                    difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1

                    if itype in {"write_the_code", "fix_the_code", "mini_challenge", "guided_project", "refactoring_challenge"}:
                        has_coding_item = True

                # Check Project lessons
                if lesson.is_project or lesson.unit_num == 42:
                    project_lessons_audited[lesson.lesson_id] = has_coding_item

                # Check DSA lessons (Units 30-41)
                if 30 <= lesson.unit_num <= 41:
                    dsa_lessons_audited[lesson.lesson_id] = has_coding_item

            except Exception as e:
                invalid_lessons[lesson.lesson_id] = [f"Audit parse failure: {e}"]

        audit_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "syllabus_coverage": {
                "total_target_lessons": total_target_lessons,
                "found_lessons": len(valid_lessons) + len(invalid_lessons),
                "valid_lessons_count": len(valid_lessons),
                "missing_lessons_count": len(missing_lessons),
                "invalid_lessons_count": len(invalid_lessons),
                "completion_percentage": round((len(valid_lessons) / total_target_lessons) * 100, 2),
            },
            "item_metrics": {
                "total_items": total_items,
                "average_items_per_lesson": round(total_items / (len(valid_lessons) + len(invalid_lessons)), 1) if (len(valid_lessons) + len(invalid_lessons)) > 0 else 0,
                "unique_item_ids": len(all_seen_item_ids),
                "duplicate_ids": duplicate_global_ids,
                "type_distribution": type_counts,
                "difficulty_distribution": difficulty_counts,
            },
            "specialized_checks": {
                "project_lessons_with_implementation": project_lessons_audited,
                "dsa_lessons_with_implementation": dsa_lessons_audited,
            },
            "missing_lessons": missing_lessons,
            "invalid_lessons": invalid_lessons,
            "lessons_with_warnings": {k: len(v) for k, v in lessons_with_warnings.items()},
        }

        # Write JSON Audit Report
        with open(json_output, "w", encoding="utf-8") as f:
            json.dump(audit_data, f, indent=2)

        # Write Human-Readable Text Report
        with open(txt_output, "w", encoding="utf-8") as f:
            f.write("============================================================\n")
            f.write("       CODOLINGO PYTHON CURRICULUM AUDIT REPORT             \n")
            f.write("============================================================\n\n")
            f.write(f"Timestamp: {audit_data['timestamp']}\n\n")
            f.write("1. SYLLABUS COMPLETION\n")
            f.write(f"   Target Syllabus Lessons: {total_target_lessons}\n")
            f.write(f"   Found Lessons:           {audit_data['syllabus_coverage']['found_lessons']}\n")
            f.write(f"   Valid Passing Lessons:   {len(valid_lessons)}\n")
            f.write(f"   Missing Lessons:         {len(missing_lessons)}\n")
            f.write(f"   Invalid Lessons:         {len(invalid_lessons)}\n")
            f.write(f"   Completion Rate:         {audit_data['syllabus_coverage']['completion_percentage']}%\n\n")

            f.write("2. ITEM METRICS\n")
            f.write(f"   Total Exercises / Items: {total_items}\n")
            f.write(f"   Average Items / Lesson:  {audit_data['item_metrics']['average_items_per_lesson']}\n")
            f.write(f"   Global Duplicate IDs:    {len(duplicate_global_ids)}\n\n")

            f.write("3. EXERCISE TYPE DISTRIBUTION\n")
            for itype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
                f.write(f"   - {itype:25}: {count}\n")
            f.write("\n")

            f.write("4. DIFFICULTY DISTRIBUTION\n")
            for diff, count in sorted(difficulty_counts.items(), key=lambda x: -x[1]):
                f.write(f"   - {diff:10}: {count}\n")
            f.write("\n")

            if invalid_lessons:
                f.write("5. INVALID LESSON DETAILS\n")
                for lid, errs in invalid_lessons.items():
                    f.write(f"   [Lesson {lid}]\n")
                    for err in errs:
                        f.write(f"     - {err}\n")
                f.write("\n")

            if missing_lessons:
                f.write(f"6. MISSING LESSONS ({len(missing_lessons)})\n")
                f.write(f"   {', '.join(missing_lessons[:50])}\n")
                if len(missing_lessons) > 50:
                    f.write(f"   ... and {len(missing_lessons) - 50} more\n")
                f.write("\n")

            f.write("============================================================\n")
            overall_pass = (len(missing_lessons) == 0 and len(invalid_lessons) == 0 and len(duplicate_global_ids) == 0)
            f.write(f"FINAL AUDIT VERDICT: {'PASSED (100% COMPLETE & VALID)' if overall_pass else 'INCOMPLETE OR HAS ERRORS'}\n")
            f.write("============================================================\n")

        print(f"[CurriculumAuditor] Audit complete. Reports saved to {json_output} and {txt_output}.")
        return audit_data
