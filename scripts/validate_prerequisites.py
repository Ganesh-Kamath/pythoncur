"""
Deterministic Prerequisite and Dependency Graph Validator for Codolingo Curriculum.
Ensures zero circular dependencies, valid prerequisite references, and strictly monotonic progression.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Set

WORKSPACE = Path(__file__).resolve().parent.parent
CONTENT_DIR = WORKSPACE / "python_content"
SYLLABUS_PATH = WORKSPACE / "PYTHON_MASTER_SYLLABUS.txt"

def load_canonical_order() -> List[str]:
    lessons = []
    if SYLLABUS_PATH.exists():
        with open(SYLLABUS_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and line[0].isdigit() and "." in line:
                    lid = line.split()[0]
                    lessons.append(lid)
    return lessons

def validate_prerequisites() -> Dict[str, Any]:
    canonical_lessons = load_canonical_order()
    lesson_order = {lid: idx for idx, lid in enumerate(canonical_lessons)}

    results = {
        "total_lessons_checked": len(canonical_lessons),
        "prerequisite_errors": 0,
        "circular_dependencies": 0,
        "forward_references": 0,
        "error_details": []
    }

    graph: Dict[str, List[str]] = {}

    for unit_dir in sorted(CONTENT_DIR.iterdir()):
        if not unit_dir.is_dir() or not unit_dir.name.startswith("unit_"):
            continue
        for lesson_file in sorted(unit_dir.glob("*.json")):
            with open(lesson_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            lid = data.get("lesson_id")
            prereqs = data.get("prerequisites", [])

            graph[lid] = prereqs

            # Check that prerequisites exist and come strictly before this lesson
            curr_idx = lesson_order.get(lid, -1)
            for p in prereqs:
                if p not in lesson_order:
                    results["prerequisite_errors"] += 1
                    results["error_details"].append(f"Lesson {lid} references non-existent prerequisite: {p}")
                else:
                    p_idx = lesson_order[p]
                    if p_idx >= curr_idx:
                        results["forward_references"] += 1
                        results["error_details"].append(f"Lesson {lid} has forward reference to prerequisite: {p}")

    # Check for cycles via DFS
    visited = set()
    visiting = set()

    def has_cycle(node: str, path: List[str]) -> bool:
        visiting.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in visiting:
                results["circular_dependencies"] += 1
                cycle_path = " -> ".join(path + [neighbor])
                results["error_details"].append(f"Cycle detected: {cycle_path}")
                return True
            if neighbor not in visited:
                if has_cycle(neighbor, path + [neighbor]):
                    return True
        visiting.remove(node)
        visited.add(node)
        return False

    for node in graph:
        if node not in visited:
            has_cycle(node, [node])

    return results

if __name__ == "__main__":
    res = validate_prerequisites()
    print(f"Checked prerequisites across {res['total_lessons_checked']} lessons.")
    print(f"Prerequisite errors: {res['prerequisite_errors']}")
    print(f"Forward references: {res['forward_references']}")
    print(f"Circular dependencies: {res['circular_dependencies']}")
    if res["prerequisite_errors"] > 0 or res["forward_references"] > 0 or res["circular_dependencies"] > 0:
        for err in res["error_details"][:10]:
            print(f" - {err}")
        sys.exit(1)
    print("Prerequisites & DAG validation: PASS")
