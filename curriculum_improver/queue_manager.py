"""
Persistent SQLite Queue Manager for Codolingo Improvement Engine.
Maintains priority queues driven by empirical signals and curriculum health deficits.
"""

import json
import logging
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from curriculum_improver.config import config

logger = logging.getLogger("QueueManager")

@dataclass
class ImprovementTask:
    task_id: int
    task_type: str
    priority: int  # 0 to 100
    priority_tier: str  # "high", "medium", "low"
    lesson_id: str
    question_id: Optional[str]
    concept: Optional[str]
    reason: str
    evidence: str
    retry_count: int = 0

class QueueManager:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = Path(db_path or config.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self) -> None:
        """Create task queue schema in SQLite."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS improvement_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_type TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    priority_tier TEXT NOT NULL,
                    lesson_id TEXT NOT NULL,
                    question_id TEXT,
                    concept TEXT,
                    reason TEXT,
                    evidence TEXT,
                    status TEXT DEFAULT 'pending',
                    retry_count INTEGER DEFAULT 0,
                    created_at REAL,
                    updated_at REAL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status_prio ON improvement_tasks(status, priority DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_lid ON improvement_tasks(lesson_id)")

    def enqueue(
        self,
        task_type: str,
        priority: int,
        lesson_id: str,
        reason: str,
        evidence: str,
        question_id: Optional[str] = None,
        concept: Optional[str] = None,
    ) -> int:
        """Add a prioritized improvement task to the queue if not already pending."""
        priority = max(1, min(100, priority))
        tier = "high" if priority >= 70 else ("medium" if priority >= 40 else "low")
        now = time.time()

        with sqlite3.connect(self.db_path) as conn:
            # Check for existing duplicate pending task
            cur = conn.execute("""
                SELECT id, priority FROM improvement_tasks 
                WHERE task_type = ? AND lesson_id = ? AND IFNULL(question_id, '') = ? AND status = 'pending'
            """, (task_type, lesson_id, question_id or ""))
            existing = cur.fetchone()
            if existing:
                if priority > existing[1]:
                    conn.execute("""
                        UPDATE improvement_tasks
                        SET priority = ?, priority_tier = ?, updated_at = ?
                        WHERE id = ?
                    """, (priority, tier, now, existing[0]))
                return existing[0]

            cur = conn.execute("""
                INSERT INTO improvement_tasks (
                    task_type, priority, priority_tier, lesson_id,
                    question_id, concept, reason, evidence,
                    status, retry_count, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', 0, ?, ?)
            """, (
                task_type, priority, tier, lesson_id,
                question_id, concept, reason, evidence,
                now, now
            ))
            return cur.lastrowid

    def pop_highest_priority_task(self, target_lesson_id: Optional[str] = None) -> Optional[ImprovementTask]:
        """Fetch and lock the highest priority pending task, optionally filtered by lesson ID."""
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            conn.isolation_level = "EXCLUSIVE"
            if target_lesson_id:
                cur = conn.execute("""
                    SELECT id, task_type, priority, priority_tier, lesson_id, question_id, concept, reason, evidence, retry_count
                    FROM improvement_tasks
                    WHERE status = 'pending' AND lesson_id = ?
                    ORDER BY priority DESC, id ASC
                    LIMIT 1
                """, (target_lesson_id,))
            else:
                cur = conn.execute("""
                    SELECT id, task_type, priority, priority_tier, lesson_id, question_id, concept, reason, evidence, retry_count
                    FROM improvement_tasks
                    WHERE status = 'pending'
                    ORDER BY priority DESC, id ASC
                    LIMIT 1
                """)
            row = cur.fetchone()
            if not row:
                return None

            task = ImprovementTask(
                task_id=row[0],
                task_type=row[1],
                priority=row[2],
                priority_tier=row[3],
                lesson_id=row[4],
                question_id=row[5],
                concept=row[6],
                reason=row[7],
                evidence=row[8],
                retry_count=row[9],
            )

            conn.execute("""
                UPDATE improvement_tasks
                SET status = 'in_progress', updated_at = ?
                WHERE id = ?
            """, (now, task.task_id))

            return task

    def mark_completed(self, task_id: int) -> None:
        """Mark task as successfully executed."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE improvement_tasks 
                SET status = 'completed', updated_at = ?
                WHERE id = ?
            """, (time.time(), task_id))

    def mark_failed(self, task_id: int, error_msg: str, max_retries: int = 3) -> None:
        """Mark task failed; retry if under limit, else retire."""
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT retry_count, priority FROM improvement_tasks WHERE id = ?", (task_id,))
            row = cur.fetchone()
            if not row:
                return
            retries, prio = row[0], row[1]
            if retries < max_retries:
                # Requeue with slight backoff penalty
                conn.execute("""
                    UPDATE improvement_tasks 
                    SET status = 'pending', retry_count = retry_count + 1, priority = MAX(10, priority - 10), updated_at = ?
                    WHERE id = ?
                """, (now, task_id))
            else:
                conn.execute("""
                    UPDATE improvement_tasks 
                    SET status = 'failed', updated_at = ?
                    WHERE id = ?
                """, (now, task_id))

    def get_queue_counts(self) -> Dict[str, int]:
        """Return counts of pending tasks by priority tier."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("""
                SELECT priority_tier, COUNT(*) 
                FROM improvement_tasks 
                WHERE status = 'pending'
                GROUP BY priority_tier
            """)
            counts = {"high": 0, "medium": 0, "low": 0}
            for tier, c in cur.fetchall():
                if tier in counts:
                    counts[tier] = c
            counts["total"] = sum(counts.values())
            return counts
