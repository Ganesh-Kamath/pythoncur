"""
Generates the Codolingo Python Curriculum Manifest from generated content files.
"""

import json
from pathlib import Path

def generate_manifest(content_dir="python_content", output_file="manifest.json"):
    root = Path(content_dir)
    manifest = {
        "title": "Codolingo Complete Python Mastery Curriculum",
        "version": "1.0.0",
        "description": "Comprehensive, production-ready Python curriculum from foundations to advanced DSA and mastery.",
        "units": []
    }
    
    unit_dirs = sorted([d for d in root.iterdir() if d.is_dir() and d.name.startswith("unit_")])
    
    total_lessons = 0
    total_items = 0
    
    for udir in unit_dirs:
        unit_data = {
            "unit_id": udir.name,
            "title": "",
            "lessons": []
        }
        
        lesson_files = sorted(udir.glob("*.json"))
        for lfile in lesson_files:
            try:
                with open(lfile, "r", encoding="utf-8") as f:
                    ldata = json.load(f)
            except Exception as e:
                print(f"Error reading {lfile}: {e}")
                continue
                
            if not unit_data["title"]:
                unit_data["title"] = ldata.get("unit", udir.name)
                
            items = ldata.get("items", [])
            concepts = sorted(list({it.get("concept") for it in items if it.get("concept")}))
            skills = sorted(list({it.get("skill") for it in items if it.get("skill")}))
            diff_counts = {}
            for it in items:
                d = it.get("difficulty", "medium")
                diff_counts[d] = diff_counts.get(d, 0) + 1
                
            is_project = "project" in ldata.get("title", "").lower()
            
            lesson_entry = {
                "lesson_id": ldata.get("lesson_id"),
                "title": ldata.get("title"),
                "file": str(lfile.relative_to(root.parent)).replace("\\", "/"),
                "item_count": len(items),
                "is_project": is_project,
                "concepts": concepts,
                "skills": skills,
                "difficulty_distribution": diff_counts
            }
            
            unit_data["lessons"].append(lesson_entry)
            total_lessons += 1
            total_items += len(items)
            
        manifest["units"].append(unit_data)
        
    manifest["total_units"] = len(manifest["units"])
    manifest["total_lessons"] = total_lessons
    manifest["total_items"] = total_items
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Generated manifest: {output_file} with {len(manifest['units'])} units, {total_lessons} lessons, {total_items} items.")
    return manifest

if __name__ == "__main__":
    generate_manifest()
