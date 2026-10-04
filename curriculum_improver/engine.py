"""
Continuous Curriculum Improver Engine for Codolingo.
Maintains the autonomous ANALYZE → PROPOSE → GENERATE → VALIDATE → REVIEW → ACCEPT/REJECT → VERSION loop.
"""

import logging
import signal
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from curriculum_improver.config import config
from curriculum_improver.dashboard import DashboardState, TerminalDashboard
from curriculum_improver.health_tracker import HealthTracker
from curriculum_improver.laya_analyzer import LayaAnalyzer
from curriculum_improver.ollama_client import OllamaClient
from curriculum_improver.quality_gate import QualityGate
from curriculum_improver.queue_manager import QueueManager
from curriculum_improver.sarvam_reviewer import SarvamReviewer
from curriculum_improver.task_engine import TaskEngine, TaskExecutionResult
from curriculum_improver.version_manager import VersionManager
from generator.syllabus_parser import SyllabusParser

logger = logging.getLogger("ContinuousImprover")

class ContinuousImproverEngine:
    def __init__(
        self,
        queue_manager: Optional[QueueManager] = None,
        task_engine: Optional[TaskEngine] = None,
        ollama_client: Optional[OllamaClient] = None,
        sarvam_reviewer: Optional[SarvamReviewer] = None,
        laya_analyzer: Optional[LayaAnalyzer] = None,
        health_tracker: Optional[HealthTracker] = None,
        dashboard: Optional[TerminalDashboard] = None,
        syllabus_parser: Optional[SyllabusParser] = None,
    ):
        self.queue = queue_manager or QueueManager()
        self.ollama = ollama_client or OllamaClient()
        self.sarvam = sarvam_reviewer or SarvamReviewer()
        self.laya = laya_analyzer or LayaAnalyzer()
        self.health = health_tracker or HealthTracker(laya_analyzer=self.laya)
        self.syllabus = syllabus_parser or SyllabusParser()
        self.dashboard = dashboard or TerminalDashboard()

        self.tasks = task_engine or TaskEngine(
            ollama_client=self.ollama,
            sarvam_reviewer=self.sarvam,
            health_tracker=self.health,
            syllabus_parser=self.syllabus,
        )

        self.running = False
        self.dashboard_state = DashboardState(start_time=time.time())

        # Setup graceful signal handlers
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        """Handle CTRL+C gracefully without interrupting atomic disk writes."""
        print("\n\n[!] Interrupt received (CTRL+C). Stopping safely after current cycle...")
        self.running = False

    def seed_initial_curriculum_tasks(self) -> int:
        """Scan active lessons and populate priority queue based on concrete quality deficits."""
        seeded = 0
        lesson_files = sorted(config.content_dir.glob("unit_*/*.json"))
        for lfile in lesson_files:
            try:
                import json
                with open(lfile, "r", encoding="utf-8") as f:
                    ldata = json.load(f)
                lid = ldata.get("lesson_id")
                report = self.health.evaluate_lesson(ldata)

                # 1. Enqueue health audit if never audited
                self.queue.enqueue(
                    task_type="curriculum_health_audit",
                    priority=50,
                    lesson_id=lid,
                    reason="Initial baseline health audit",
                    evidence="System startup initialization",
                )
                seeded += 1

                # 2. Check for explanation quality deficit
                if report.explanation_quality < 80:
                    self.queue.enqueue(
                        task_type="improve_explanation",
                        priority=75,
                        lesson_id=lid,
                        reason="Explanation completeness deficit (<80%)",
                        evidence=f"Current explanation score: {report.explanation_quality}",
                    )
                    seeded += 1

                # 3. Check for missing hints in coding items
                coding_items_without_hints = [
                    it for it in ldata.get("items", [])
                    if it.get("type") in {"fix_the_code", "write_the_code"} and not it.get("hint")
                ]
                if coding_items_without_hints:
                    target_q = coding_items_without_hints[0]
                    self.queue.enqueue(
                        task_type="generate_hints",
                        priority=65,
                        lesson_id=lid,
                        question_id=target_q.get("id"),
                        reason="Hands-on coding exercise lacks progressive hint",
                        evidence=f"Question {target_q.get('id')} has no hint",
                    )
                    seeded += 1

            except Exception as e:
                logger.warning(f"Error seeding tasks from {lfile.name}: {e}")
                continue

        return seeded

    def run_continuous(self, max_cycles: Optional[int] = None, target_lesson_id: Optional[str] = None) -> None:
        """Execute the continuous autonomous improvement loop."""
        self.running = True
        self.dashboard_state.start_time = time.time()

        # Seed initial queue if empty
        counts = self.queue.get_queue_counts()
        if counts["total"] == 0:
            print("[Curriculum Lab] Queue empty. Inspecting curriculum to seed tasks...")
            seeded_count = self.seed_initial_curriculum_tasks()
            print(f"[Curriculum Lab] Seeded {seeded_count} improvement tasks based on curriculum health audits.")
            counts = self.queue.get_queue_counts()

        print("\n[Curriculum Lab] Starting continuous improvement engine. Press CTRL+C to stop.\n")

        cycle = 0
        while self.running:
            cycle += 1
            if max_cycles and cycle > max_cycles:
                break

            # 1. Update Subsystem Status
            self.dashboard_state.qwen_online = self.ollama.is_online()
            self.dashboard_state.sarvam_online = self.sarvam.is_online()
            self.dashboard_state.laya_online = self.laya.has_telemetry_data()

            # 2. Update Queue Metrics
            counts = self.queue.get_queue_counts()
            self.dashboard_state.queue_high = counts["high"]
            self.dashboard_state.queue_medium = counts["medium"]
            self.dashboard_state.queue_low = counts["low"]

            # If queue depleted, re-audit
            if counts["total"] == 0:
                print("[Curriculum Lab] Queue empty. Running periodic health scan...")
                self.seed_initial_curriculum_tasks()
                counts = self.queue.get_queue_counts()

            # 3. Select Highest-Priority Task
            task = self.queue.pop_highest_priority_task(target_lesson_id=target_lesson_id)
            if not task:
                time.sleep(config.sleep_between_cycles)
                continue

            # Update dashboard active task
            self.dashboard_state.current_lesson = task.lesson_id
            lesson_info = self.syllabus.get_lesson(task.lesson_id)
            self.dashboard_state.current_unit = f"Unit {lesson_info.unit_num}" if lesson_info else "Curriculum"
            self.dashboard_state.current_task = f"{task.task_type} (Prio: {task.priority})"
            self.dashboard_state.current_question = task.question_id

            # Render Dashboard
            self.dashboard.render(self.dashboard_state)

            # 4. Execute Task (ANALYZE → PROPOSE → VALIDATE → REVIEW → ACCEPT/REJECT → VERSION)
            result = self.tasks.execute_task(task)

            # 5. Process Outcome
            self.dashboard_state.cycles_completed += 1
            if result.accepted:
                self.dashboard_state.accepted_count += 1
                self.dashboard_state.last_change_id = f"{result.lesson_id} ({result.question_id or 'lesson'})"
                self.dashboard_state.last_health_before = result.health_before
                self.dashboard_state.last_health_after = result.health_after
                self.queue.mark_completed(task.task_id)
                print(f"\033[92m[ACCEPTED]\033[0m {result.message}")
            else:
                self.dashboard_state.rejected_count += 1
                self.queue.mark_failed(task.task_id, result.message)
                print(f"\033[91m[REJECTED]\033[0m {result.message}")

            # Sleep between cycles to prevent busy looping
            time.sleep(config.sleep_between_cycles)

        # On Exit
        self._print_exit_summary()

    def _print_exit_summary(self) -> None:
        """Print clean summary on graceful exit."""
        elapsed = time.time() - self.dashboard_state.start_time
        duration = self.dashboard.format_duration(elapsed)
        print(f"""
==============================================================
               CURRICULUM LAB SAFELY STOPPED                  
==============================================================
  Total Runtime:    {duration}
  Total Cycles:     {self.dashboard_state.cycles_completed}
  Accepted Changes: {self.dashboard_state.accepted_count}
  Rejected Changes: {self.dashboard_state.rejected_count}
  All state, versions, and logs safely preserved on disk.
==============================================================
""")
