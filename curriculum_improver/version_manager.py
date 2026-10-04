"""
Version Manager for Codolingo Improvement Engine.
Maintains an immutable version history of all curriculum revisions and audit trails.
"""

import json
import logging
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from curriculum_improver.config import config

logger = logging.getLogger("VersionManager")

class VersionManager:
    def __init__(self):
        config.ensure_directories()
        self.versions_root = config.versions_dir
        self.logs_dir = config.logs_dir
        self.rejected_dir = config.rejected_dir
        self.reports_dir = config.reports_dir

    def _get_lesson_versions_dir(self, lesson_id: str) -> Path:
        """Return directory for a lesson's versions, e.g. data/curriculum/versions/lesson_1_3/"""
        clean_id = lesson_id.replace(".", "_")
        vdir = self.versions_root / f"lesson_{clean_id}"
        vdir.mkdir(parents=True, exist_ok=True)
        return vdir

    def ensure_initial_version(self, lesson_id: str, lesson_file: Path) -> Path:
        """Create v001.json baseline snapshot from active lesson file if not present."""
        vdir = self._get_lesson_versions_dir(lesson_id)
        v1_path = vdir / "v001.json"
        if not v1_path.exists() and lesson_file.exists():
            shutil.copyfile(lesson_file, v1_path)
            logger.info(f"Initialized baseline version v001 for {lesson_id}")
        return v1_path

    def get_latest_version_num(self, lesson_id: str) -> int:
        """Determine latest version number for a lesson (e.g. 2 for v002.json)."""
        vdir = self._get_lesson_versions_dir(lesson_id)
        versions = list(vdir.glob("v*.json"))
        if not versions:
            return 0
        nums = []
        for v in versions:
            stem = v.stem  # e.g. "v001"
            if stem.startswith("v") and stem[1:].isdigit():
                nums.append(int(stem[1:]))
        return max(nums) if nums else 0

    def commit_accepted_change(
        self,
        lesson_id: str,
        active_filepath: Path,
        new_lesson_dict: Dict[str, Any],
        question_id: Optional[str],
        reason: str,
        evidence: str,
        model_used: str,
        validation_passed: bool,
        sarvam_review: Dict[str, Any],
        score_before: int,
        score_after: int,
    ) -> Path:
        """
        Record a validated & accepted change as a new version and update the active curriculum file.
        """
        vdir = self._get_lesson_versions_dir(lesson_id)
        self.ensure_initial_version(lesson_id, active_filepath)

        next_ver = self.get_latest_version_num(lesson_id) + 1
        new_ver_filename = f"v{next_ver:03d}.json"
        new_ver_path = vdir / new_ver_filename

        # Write version snapshot
        with open(new_ver_path, "w", encoding="utf-8") as f:
            json.dump(new_lesson_dict, f, indent=2)

        # Atomically update active lesson file in python_content/
        temp_dir = active_filepath.parent
        with tempfile.NamedTemporaryFile("w", dir=temp_dir, delete=False, encoding="utf-8") as tf:
            json.dump(new_lesson_dict, tf, indent=2)
            temp_name = tf.name
        shutil.move(temp_name, active_filepath)

        # Write detailed improvement log entry
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "lesson_id": lesson_id,
            "question_id": question_id,
            "old_version": f"v{next_ver - 1:03d}",
            "new_version": f"v{next_ver:03d}",
            "reason": reason,
            "evidence": evidence,
            "model_used": model_used,
            "validation_passed": validation_passed,
            "sarvam_review": sarvam_review,
            "quality_score_before": score_before,
            "quality_score_after": score_after,
        }
        log_file = self.logs_dir / f"{timestamp_str}_{lesson_id.replace('.', '_')}.json"
        with open(log_file, "w", encoding="utf-8") as lf:
            json.dump(log_entry, lf, indent=2)

        logger.info(f"[VersionManager] Accepted change committed: {lesson_id} -> {new_ver_filename} (Score: {score_before} -> {score_after})")
        return new_ver_path

    def log_rejected_proposal(
        self,
        lesson_id: str,
        question_id: Optional[str],
        proposed_item_or_lesson: Dict[str, Any],
        reason: str,
        evidence: str,
        model_used: str,
        validation_errors: List[str],
        sarvam_review: Optional[Dict[str, Any]],
        rejection_cause: str,
    ) -> Path:
        """Record rejected change proposal with full evidence for offline analysis."""
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "lesson_id": lesson_id,
            "question_id": question_id,
            "rejection_cause": rejection_cause,
            "reason": reason,
            "evidence": evidence,
            "model_used": model_used,
            "validation_errors": validation_errors,
            "sarvam_review": sarvam_review,
            "proposed_data": proposed_item_or_lesson,
        }
        rej_file = self.rejected_dir / f"{timestamp_str}_{lesson_id.replace('.', '_')}_rejected.json"
        with open(rej_file, "w", encoding="utf-8") as rf:
            json.dump(record, rf, indent=2)

        logger.info(f"[VersionManager] Proposal rejected and logged: {lesson_id} ({rejection_cause})")
        return rej_file

    def save_health_report(self, lesson_id: str, report_markdown: str) -> Path:
        """Persist health audit report for a lesson."""
        clean_id = lesson_id.replace(".", "_")
        report_file = self.reports_dir / f"health_{clean_id}.txt"
        report_file.write_text(report_markdown, encoding="utf-8")
        return report_file
