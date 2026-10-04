"""
Observability Terminal Dashboard for Codolingo Improvement Engine.
Renders real-time telemetry, model status, task queue health, and quality deltas.
"""

import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class DashboardState:
    start_time: float
    cycles_completed: int = 0
    accepted_count: int = 0
    rejected_count: int = 0
    current_unit: str = "Unit 1"
    current_lesson: str = "1.1"
    current_task: str = "idle"
    current_question: Optional[str] = None
    queue_high: int = 0
    queue_medium: int = 0
    queue_low: int = 0
    qwen_online: bool = False
    sarvam_online: bool = False
    laya_online: bool = False
    last_change_id: str = "None"
    last_health_before: int = 0
    last_health_after: int = 0

class TerminalDashboard:
    def __init__(self):
        pass

    @staticmethod
    def format_duration(seconds: float) -> str:
        s = int(seconds)
        hours = s // 3600
        minutes = (s % 3600) // 60
        secs = s % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def render(self, state: DashboardState) -> None:
        """Render a clean ANSI dashboard to the console."""
        elapsed = time.time() - state.start_time
        runtime_str = self.format_duration(elapsed)

        qwen_badge = "[ONLINE]" if state.qwen_online else "[OFFLINE]"
        sarvam_badge = "[ONLINE]" if state.sarvam_online else "[OFFLINE]"
        laya_badge = "[ONLINE]" if state.laya_online else "[STANDBY]"

        q_info = f"Question: {state.current_question}" if state.current_question else ""

        delta = state.last_health_after - state.last_health_before
        delta_str = f"(+{delta})" if delta >= 0 else f"({delta})"

        output = f"""
==============================================================
                 CODOLINGO CURRICULUM LAB                     
==============================================================
  Runtime:  {runtime_str:<12} | Cycles:   {state.cycles_completed:<8}
  Accepted: {state.accepted_count:<12} | Rejected: {state.rejected_count:<8}
──────────────────────────────────────────────────────────────
  Current Action:
  Location: {state.current_unit} -> Lesson {state.current_lesson}
  Task:     {state.current_task}
  {q_info}

  Priority Queue:
  [HIGH] {state.queue_high:<3} High Priority  |  [MED] {state.queue_medium:<3} Med Priority  |  [LOW] {state.queue_low:<3} Low Priority

  Model Subsystems:
  Local Qwen3 8B: {qwen_badge}  |  Sarvam 105B: {sarvam_badge}  |  Laya Memory: {laya_badge}

  Last Curriculum Change:
  Target: {state.last_change_id}
  Health: {state.last_health_before} -> {state.last_health_after} {delta_str}
──────────────────────────────────────────────────────────────
  Press CTRL+C anytime to stop safely after the current cycle.
"""
        print(output)
