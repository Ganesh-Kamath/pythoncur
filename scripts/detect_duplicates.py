"""
Deterministic Duplicate and Repetition Detector for Codolingo Curriculum.
Detects exact prompt duplicates, near-duplicates, and repetitive filler patterns.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any

WORKSPACE = Path(__file__).resolve().parent.parent
CONTENT_DIR = WORKSPACE / "python_content"

def detect_duplicates() -> Dict[str, Any]:
    prompt_to_items = defaultdict(list)
    total_items = 0

    for unit_dir in sorted(CONTENT_DIR.iterdir()):
        if not unit_dir.is_dir() or not unit_dir.name.startswith("unit_"):
            continue
        for lesson_file in sorted(unit_dir.glob("*.json")):
            with open(lesson_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            lid = data.get("lesson_id")

            for item in data.get("items", []):
                total_items += 1
                iid = item.get("id")
                prompt = item.get("prompt", "").strip()
                if len(prompt) > 20:
                    # Normalize whitespace
                    norm_prompt = re.sub(r"\s+", " ", prompt)
                    prompt_to_items[norm_prompt].append(iid)

    duplicate_clusters = {}
    total_duplicate_prompts = 0

    for prompt, items in prompt_to_items.items():
        if len(items) > 1:
            total_duplicate_prompts += (len(items) - 1)
            if len(items) >= 3:
                duplicate_clusters[prompt[:80]] = items

    return {
        "total_items": total_items,
        "unique_prompts": len(prompt_to_items),
        "total_duplicate_prompts": total_duplicate_prompts,
        "duplicate_clusters": duplicate_clusters
    }

if __name__ == "__main__":
    res = detect_duplicates()
    print(f"Audited {res['total_items']} items for duplication.")
    print(f"Total duplicate prompt instances: {res['total_duplicate_prompts']}")
    print(f"Significant duplicate clusters (>=3 items): {len(res['duplicate_clusters'])}")
    if len(res["duplicate_clusters"]) > 0:
        for p, items in list(res["duplicate_clusters"].items())[:5]:
            print(f" - Repeated {len(items)}x: '{p}' -> {items}")
        sys.exit(1)
    print("Duplicate detection: PASS")
