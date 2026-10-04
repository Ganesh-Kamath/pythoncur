#!/usr/bin/env python3
"""
Codolingo Overnight Production Curriculum Generator.
Autonomous, continuous generation of ~7,320 curriculum items across 244 lessons (43 sections).

Usage:
  python scripts/generate_curriculum.py           # Production Continuous Overnight Run
  python scripts/generate_curriculum.py --test    # Test Mode (4 diverse lesson archetypes)
  python scripts/generate_curriculum.py --status  # Progress & Health Status
  python scripts/generate_curriculum.py --lesson 4.1  # Target a single lesson
"""

import argparse
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Force UTF-8 stdout encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True, write_through=True)
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True, write_through=True)
    except Exception:
        pass

from generator.production_generator import ProductionGenerator
from generator.syllabus_parser import LessonInfo


class TerminalDashboard:
    """ASCII-safe, rich observability dashboard for overnight monitoring."""

    @staticmethod
    def render(
        completed: int,
        total: int,
        items: int,
        target_items: int,
        current_lesson: Optional[LessonInfo],
        stage: str,
        qwen_status: str,
        sarvam_status: str,
        laya_status: str,
        last_lesson_info: str,
        last_review_info: str,
        start_time: float,
        accepted: int,
        rejected: int,
        repaired: int,
    ) -> None:
        pct = (completed / total * 100) if total else 0.0
        bar_len = 20
        filled = int(bar_len * (completed / total)) if total else 0
        progress_bar = "[" + "#" * filled + "-" * (bar_len - filled) + "]"

        elapsed_secs = int(time.time() - start_time)
        hrs = elapsed_secs // 3600
        mins = (elapsed_secs % 3600) // 60
        secs = elapsed_secs % 60
        runtime_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"

        cur_str = f"Unit {current_lesson.unit_num} -> Lesson {current_lesson.lesson_id} ({current_lesson.title})" if current_lesson else "None (All Complete)"

        print("\n" + "=" * 62)
        print("           CODOLINGO OVERNIGHT CURRICULUM LAB                 ")
        print("=" * 62)
        print(f"  Progress: {progress_bar} {pct:5.1f}% ({completed}/{total} lessons)")
        print(f"  Items:    {items:,} / ~{target_items:,} target items")
        print(f"  Runtime:  {runtime_str}  |  Accepted: {accepted}  |  Repaired: {repaired}")
        print("─" * 62)
        print("  Current Action:")
        print(f"  Target:   {cur_str}")
        print(f"  Stage:    {stage}")
        print()
        print("  Subsystems:")
        print(f"  Qwen3 8B: [{qwen_status}]   |   Sarvam 105B: [{sarvam_status}]   |   Laya: [{laya_status}]")
        print()
        print("  Last Lesson Result:")
        print(f"  Status:   {last_lesson_info}")
        print(f"  Review:   {last_review_info}")
        print("─" * 62)
        print("  Press CTRL+C anytime to stop safely after the current cycle.")
        print("=" * 62 + "\n")


def run_test_mode(generator: ProductionGenerator) -> None:
    """
    Test Mode: Runs 4 distinct lesson archetypes:
      1. Beginner lesson: 4.1 (The input() Function)
      2. Intermediate lesson: 12.1 (Defining Functions)
      3. DSA lesson: 21.1 (Big O Notation and Time Complexity)
      4. Project lesson: 5.6 (Project: Interactive Calculator)
    """
    print("\n" + "=" * 62)
    print("      CODOLINGO GENERATOR PRE-FLIGHT TEST MODE (4 ARCHETYPES) ")
    print("=" * 62)

    test_ids = ["4.1", "12.1", "21.1", "5.6"]
    results = []

    for lid in test_ids:
        lesson = generator.syllabus.lessons_by_id.get(lid)
        if not lesson:
            print(f"[WARN] Test lesson {lid} not found in syllabus. Skipping.")
            continue

        print(f"\n>>> Running Test on Archetype: Lesson {lid} - {lesson.title} ({lesson.unit_title}) [Project: {lesson.is_project}]")
        t0 = time.time()
        success, msg = generator.generate_single_lesson(lesson, force=True)
        duration = time.time() - t0

        dest_file = generator.get_lesson_filepath(lesson)
        val_res = generator.validator.validate_file(dest_file)

        results.append({
            "lesson_id": lid,
            "title": lesson.title,
            "is_project": lesson.is_project,
            "success": success,
            "valid": val_res.valid,
            "items": len(val_res.errors) if not val_res.valid else 30,
            "duration": f"{duration:.1f}s",
            "message": msg,
        })

    print("\n" + "=" * 62)
    print("                 PRE-FLIGHT TEST SUMMARY                      ")
    print("=" * 62)
    all_passed = True
    for r in results:
        status_badge = "[PASS]" if (r["success"] and r["valid"]) else "[FAIL]"
        if not (r["success"] and r["valid"]):
            all_passed = False
        p_tag = " (PROJECT)" if r["is_project"] else ""
        print(f"  {status_badge} Lesson {r['lesson_id']}{p_tag}: {r['title']} in {r['duration']}")

    print("─" * 62)
    if all_passed:
        print("  All 4 archetypes successfully generated, validated, and verified!")
        print("  System is fully primed and ready for overnight production run:")
        print("  Command: python scripts/generate_curriculum.py")
    else:
        print("  One or more test lessons failed validation. Review logs before overnight run.")
    print("=" * 62 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Codolingo Overnight Production Curriculum Generator")
    parser.add_argument("--test", action="store_true", help="Run 4-lesson archetype validation test")
    parser.add_argument("--status", action="store_true", help="Print current curriculum generation progress")
    parser.add_argument("--lesson", type=str, default=None, help="Target a specific lesson ID (e.g. 4.1)")
    parser.add_argument("--force", action="store_true", help="Force regenerate lesson even if completed")
    args = parser.parse_args()

    generator = ProductionGenerator()
    start_time = time.time()
    running = True

    def sigint_handler(signum, frame):
        nonlocal running
        print("\n\n[SHUTDOWN] CTRL+C detected. Gracefully completing current operation and saving state...")
        running = False

    signal.signal(signal.SIGINT, sigint_handler)

    # 1. Status mode
    if args.status:
        completed, total, items = generator.state.get_progress()
        print("\n" + "=" * 50)
        print("       CODOLINGO CURRICULUM PROGRESS REPORT       ")
        print("=" * 50)
        print(f"  Lessons Completed: {completed} / {total} ({(completed / total * 100):.1f}%)")
        print(f"  Items Generated:   {items:,} / ~{total * 30:,}")
        print(f"  Active Units:      {len(generator.syllabus.units)}")
        print(f"  State Database:    {generator.state.state_path}")
        print("=" * 50 + "\n")
        return

    # 2. Test mode
    if args.test:
        run_test_mode(generator)
        return

    # 3. Single lesson mode
    if args.lesson:
        lesson = generator.syllabus.lessons_by_id.get(args.lesson)
        if not lesson:
            print(f"[ERROR] Lesson '{args.lesson}' not found in master syllabus.")
            sys.exit(1)
        print(f"Targeting single lesson: {lesson.lesson_id} - {lesson.title}")
        success, msg = generator.generate_single_lesson(lesson, force=args.force)
        print(f"Result: {msg}")
        return

    # 4. Continuous Overnight Production Mode
    print("\n[Codolingo Production] Starting autonomous overnight curriculum engine...")
    last_lesson_info = "Ready"
    last_review_info = "Pending"

    all_lessons = list(generator.syllabus.lessons_by_id.values())

    while running:
        completed, total, items = generator.state.get_progress()

        # Check if all lessons completed
        if completed >= total:
            print("\n[MILESTONE] All 244 lessons exist on disk! Transitioning to QUALITY IMPROVEMENT MODE...")
            # Hand off to quality improver loop
            try:
                from curriculum_improver.engine import ContinuousImproverEngine
                improver = ContinuousImproverEngine()
                improver.run_continuous()
            except KeyboardInterrupt:
                pass
            break

        # Find next incomplete lesson
        next_lesson = None
        for lesson in all_lessons:
            if not generator.state.is_completed(lesson.lesson_id):
                next_lesson = lesson
                break

        if not next_lesson:
            break

        # Update terminal dashboard
        qwen_stat = "ONLINE" if generator.ollama.is_online() else "OFFLINE"
        sarvam_stat = "ONLINE" if generator.sarvam.is_online() else "STANDBY"
        laya_stat = "ACTIVE"
        accepted = generator.state.data["stats"].get("accepted_count", 0)
        rejected = generator.state.data["stats"].get("rejected_count", 0)
        repaired = generator.state.data["stats"].get("repaired_count", 0)

        TerminalDashboard.render(
            completed=completed,
            total=total,
            items=items,
            target_items=total * 30,
            current_lesson=next_lesson,
            stage="Generating 30 curriculum items via 3-layer pipeline",
            qwen_status=qwen_stat,
            sarvam_status=sarvam_stat,
            laya_status=laya_stat,
            last_lesson_info=last_lesson_info,
            last_review_info=last_review_info,
            start_time=start_time,
            accepted=accepted,
            rejected=rejected,
            repaired=repaired,
        )

        # Generate single lesson
        success, msg = generator.generate_single_lesson(next_lesson)
        if success:
            last_lesson_info = f"{next_lesson.lesson_id} [PASS] (30 items)"
            last_review_info = "Accepted by Quality Gate & Review"
        else:
            last_lesson_info = f"{next_lesson.lesson_id} [FAIL]"
            last_review_info = msg[:50]

        # Polite breathing delay between lessons to prevent host CPU spikes
        time.sleep(1.0)

    # Clean shutdown summary
    completed, total, items = generator.state.get_progress()
    print("\n" + "=" * 62)
    print("           OVERNIGHT GENERATION SAFELY PAUSED                 ")
    print("=" * 62)
    print(f"  Total Lessons Completed: {completed} / {total} ({(completed / total * 100):.1f}%)")
    print(f"  Total Items Generated:   {items:,} / ~{total * 30:,}")
    print(f"  Accepted:                {generator.state.data['stats'].get('accepted_count', 0)}")
    print(f"  Repaired:                {generator.state.data['stats'].get('repaired_count', 0)}")
    print(f"  Rejected / Retried:      {generator.state.data['stats'].get('rejected_count', 0)}")
    print(f"  State & Versions:        All safe on disk in data/")
    print("=" * 62 + "\n")


if __name__ == "__main__":
    main()
