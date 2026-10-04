"""
Main CLI Entry Point for Codolingo Python Curriculum Generation System.
Designed for first-class standalone execution in Windows Terminal / PowerShell / Command Prompt.
"""

import argparse
import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from generator.audit import CurriculumAuditor
from generator.curriculum_generator import CurriculumGenerator
from generator.sarvam_client import SarvamClient
from generator.state_manager import StateManager
from generator.syllabus_parser import SyllabusParser
from generator.validator import CurriculumValidator

def print_banner():
    banner = r"""
  ==============================================================
   ____          _       _ _                    ____  _   _ 
  / ___|___   __| | ___ | (_)_ __   __ _  ___  |  _ \| | | |
 | |   / _ \ / _` |/ _ \| | | '_ \ / _` |/ _ \ | |_) | |_| |
 | |__| (_) | (_| | (_) | | | | | | (_| | (_) ||  __/|  _  |
  \____\___/ \__,_|\___/|_|_|_| |_|\__, |\___/ |_|   |_| |_|
                                   |___/                    
        Complete Python Curriculum Generator (1.1 - 43.5)
  ==============================================================
"""
    print(banner)

def main():
    parser = argparse.ArgumentParser(
        description="Codolingo Python Curriculum Generator - Standalone CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generator/main.py               # Start generating curriculum sequentially
  python generator/main.py --resume      # Resume from first incomplete lesson
  python generator/main.py --lesson 1.3  # Generate or re-generate specific lesson 1.3
  python generator/main.py --unit 1      # Generate all lessons for Unit 1
  python generator/main.py --validate    # Validate all existing curriculum files
  python generator/main.py --audit       # Run full audit and write audit reports
  python generator/main.py --sync        # Synchronize generation_state.json with files on disk
        """
    )

    parser.add_argument("--resume", action="store_true", help="Resume generation from the first incomplete lesson")
    parser.add_argument("--lesson", type=str, default=None, help="Generate a specific lesson (e.g. --lesson 1.3)")
    parser.add_argument("--unit", type=int, default=None, help="Generate all lessons for a specific unit (e.g. --unit 1)")
    parser.add_argument("--validate", action="store_true", help="Run local validation on all existing curriculum files")
    parser.add_argument("--audit", action="store_true", help="Run complete curriculum audit and generate audit reports")
    parser.add_argument("--force", action="store_true", help="Force regeneration of lesson even if already completed")
    parser.add_argument("--sync", action="store_true", help="Synchronize state manager with existing files on disk")
    parser.add_argument("--retry-failed", action="store_true", help="Retry all previously failed lessons recorded in state")

    args = parser.parse_args()

    print_banner()

    state = StateManager()
    syllabus = SyllabusParser()
    validator = CurriculumValidator()
    content_dir = Path("python_content")

    # 1. Sync option
    if args.sync:
        print("[State] Synchronizing state with files in python_content/...")
        count = state.sync_with_filesystem(content_dir)
        print(f"[State] Synced {count} existing lesson files. Completed: {len(state.state['lessons_completed'])}")
        return

    # 2. Validation option
    if args.validate:
        print("Running comprehensive curriculum validation...")
        all_files = sorted(content_dir.glob("unit_*/*.json"))
        total = len(all_files)
        passed = 0
        failed = 0

        print(f"Found {total} lesson file(s) to validate.\n")
        for fpath in all_files:
            res = validator.validate_file(fpath)
            if res.valid:
                passed += 1
                warn_str = f" ({len(res.warnings)} warnings)" if res.warnings else ""
                print(f"[PASS] {fpath.name}{warn_str}")
            else:
                failed += 1
                print(f"[FAIL] {fpath.name} ({len(res.errors)} errors):")
                for err in res.errors:
                    print(f"       - {err}")

        print("\n--------------------------------------------------------------")
        print(f"Validation Summary: {passed}/{total} Passed, {failed} Failed.")
        sys.exit(0 if failed == 0 else 1)

    # 3. Audit option
    if args.audit:
        print("Running full curriculum audit...")
        auditor = CurriculumAuditor(content_dir=content_dir, syllabus_parser=syllabus)
        auditor.run_audit()
        return

    # 4. Check for API Key before generation
    client = SarvamClient()
    if not client.has_api_key():
        print("[!] ERROR: SARVAM_API_KEY is not set or empty in .env!")
        print("    Please open .env and add your Sarvam API subscription key:")
        print("    SARVAM_API_KEY=your_actual_key_here")
        print("    SARVAM_MODEL=Sarvam-105B\n")
        sys.exit(1)

    generator = CurriculumGenerator(
        content_dir=content_dir,
        sarvam_client=client,
        validator=validator,
        state_manager=state,
        syllabus_parser=syllabus,
    )

    try:
        # 5. Retry failed option
        if args.retry_failed:
            failed_lessons = list(state.state.get("failed_lessons", {}).keys())
            if not failed_lessons:
                print("No failed lessons recorded in generation_state.json!")
                return
            print(f"Retrying {len(failed_lessons)} previously failed lessons: {failed_lessons}")
            for lid in failed_lessons:
                generator.generate_specific_lesson(lid, force=True)
            return

        # 6. Specific lesson option
        if args.lesson:
            print(f"Targeting single lesson: {args.lesson}")
            success = generator.generate_specific_lesson(args.lesson, force=args.force)
            sys.exit(0 if success else 1)

        # 7. Specific unit option
        if args.unit is not None:
            print(f"Targeting Unit {args.unit}")
            generator.generate_unit(args.unit, force=args.force)
            return

        # 8. Default: Full generation / Resume
        resume_mode = args.resume or True  # Safe default to resume
        generator.generate_all(resume=resume_mode, force=args.force)

    except KeyboardInterrupt:
        print("\n\n[!] Process interrupted by user (Ctrl+C).")
        print("    Current progress safely saved in generation_state.json and local files.")
        print("    You can resume anytime by running: python generator/main.py --resume\n")
        state.save()
        sys.exit(0)

if __name__ == "__main__":
    main()
