"""
Standalone Entry Point for Codolingo Continuous Curriculum Improvement Engine.
Executable directly from Windows Terminal / PowerShell / Command Prompt.
"""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Ensure safe UTF-8 encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from curriculum_improver.config import config
from curriculum_improver.engine import ContinuousImproverEngine
from curriculum_improver.health_tracker import HealthTracker
from curriculum_improver.queue_manager import QueueManager
from curriculum_improver.sarvam_reviewer import SarvamReviewer
from curriculum_improver.ollama_client import OllamaClient

def main():
    parser = argparse.ArgumentParser(
        description="Codolingo Continuous Curriculum Improvement Lab",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/curriculum_improver.py                # Run continuously until CTRL+C
  python scripts/curriculum_improver.py --max-cycles 1 # Run a single cycle (test run)
  python scripts/curriculum_improver.py --lesson 1.3   # Target improvements on Lesson 1.3
  python scripts/curriculum_improver.py --audit        # Generate health reports for all lessons
  python scripts/curriculum_improver.py --status       # Print queue and subsystem status
        """
    )

    parser.add_argument("--max-cycles", type=int, default=None, help="Maximum number of improvement cycles to run")
    parser.add_argument("--lesson", type=str, default=None, help="Target improvements to a specific lesson (e.g. 1.3)")
    parser.add_argument("--task", type=str, default="generate_hints", help="Task type to execute (default: generate_hints)")
    parser.add_argument("--question", type=str, default=None, help="Target specific question ID (e.g. 1.3_q15)")
    parser.add_argument("--audit", action="store_true", help="Run health evaluation and print reports for existing lessons")
    parser.add_argument("--status", action="store_true", help="Print queue counts and model availability")

    args = parser.parse_args()

    config.ensure_directories()

    # 1. Status command
    if args.status:
        ollama = OllamaClient()
        sarvam = SarvamReviewer()
        queue = QueueManager()
        counts = queue.get_queue_counts()

        print("\n==============================================================")
        print("          CODOLINGO CURRICULUM LAB STATUS                     ")
        print("==============================================================")
        print(f"  Local Qwen3 8B (Ollama): {'ONLINE' if ollama.is_online() else 'OFFLINE'}")
        print(f"  Sarvam Reviewer:         {'ONLINE' if sarvam.is_online() else 'OFFLINE'}")
        print(f"  Pending Queue Items:     {counts['total']} ([HIGH] {counts['high']}, [MED] {counts['medium']}, [LOW] {counts['low']})")
        print(f"  Data Storage:            {config.data_dir.resolve()}")
        print("==============================================================\n")
        return

    # 2. Audit command
    if args.audit:
        print("\nEvaluating curriculum health across all active lessons...")
        tracker = HealthTracker()
        lesson_files = sorted(config.content_dir.glob("unit_*/*.json"))
        for lf in lesson_files:
            try:
                import json
                with open(lf, "r", encoding="utf-8") as f:
                    ldata = json.load(f)
                rep = tracker.evaluate_lesson(ldata)
                status_icon = "[PASS]" if rep.overall_health >= 80 else ("[WARN]" if rep.overall_health >= 65 else "[FAIL]")
                print(f"  {status_icon:<6} Lesson {rep.lesson_id:<5} ({rep.lesson_title:<32}) | Health: {rep.overall_health:>3}/100")
            except Exception as e:
                print(f"  [ERROR] Could not evaluate {lf.name}: {e}")
        print("\nAudit completed.\n")
        return

    # 3. Target single lesson
    if args.lesson:
        engine = ContinuousImproverEngine()
        target_task = args.task or "generate_hints"
        print(f"\nTargeting {target_task} on Lesson {args.lesson} (question: {args.question or 'auto-detect'})...")
        engine.queue.enqueue(
            task_type=target_task,
            priority=99,
            lesson_id=args.lesson,
            question_id=args.question,
            reason=f"Targeted single run for {args.lesson} ({target_task})",
            evidence="Manual CLI targeting",
        )
        engine.run_continuous(max_cycles=args.max_cycles or 1, target_lesson_id=args.lesson)
        return

    # 4. Continuous autonomous run
    engine = ContinuousImproverEngine()
    engine.run_continuous(max_cycles=args.max_cycles)

if __name__ == "__main__":
    main()
