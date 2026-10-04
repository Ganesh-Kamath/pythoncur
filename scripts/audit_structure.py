import re
import json
from pathlib import Path

def check_structure():
    syllabus_path = Path("PYTHON_MASTER_SYLLABUS.txt")
    with open(syllabus_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    syllabus_units = {}
    current_unit = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        um = re.match(r"^(\d+)\.\s+(.*)$", line)
        if um:
            u_num = int(um.group(1))
            u_title = um.group(2).strip()
            current_unit = u_num
            syllabus_units[current_unit] = {"title": u_title, "lessons": []}
            continue
        lm = re.match(r"^(\d+\.\d+)\s+(.*)$", line)
        if lm and current_unit is not None:
            lid = lm.group(1).strip()
            ltitle = lm.group(2).strip()
            syllabus_units[current_unit]["lessons"].append({"id": lid, "title": ltitle})

    print(f"Syllabus Units: {len(syllabus_units)}")
    total_syl_lessons = sum(len(u["lessons"]) for u in syllabus_units.values())
    print(f"Syllabus Lessons: {total_syl_lessons}")

    content_dir = Path("python_content")
    disk_units = sorted([d for d in content_dir.iterdir() if d.is_dir()])
    print(f"Disk Unit Folders: {len(disk_units)}")

    mismatches = []
    metadata_mismatches = []

    for u_num, u_data in syllabus_units.items():
        u_folder = content_dir / f"unit_{u_num:02d}"
        if not u_folder.exists():
            mismatches.append(f"Missing folder: {u_folder.name}")
            continue
        
        json_files = list(u_folder.glob("*.json"))
        if len(json_files) != len(u_data["lessons"]):
            mismatches.append(
                f"Unit {u_num:02d} ({u_data['title']}): expected {len(u_data['lessons'])} files, found {len(json_files)}"
            )

        for s_les in u_data["lessons"]:
            lid = s_les["id"]
            matching = [f for f in json_files if f.name.startswith(f"{lid}_")]
            if not matching:
                mismatches.append(f"Unit {u_num:02d}: Missing file for Lesson {lid} ({s_les['title']})")
            elif len(matching) > 1:
                mismatches.append(f"Unit {u_num:02d}: Multiple files for Lesson {lid}: {[f.name for f in matching]}")
            else:
                target_file = matching[0]
                try:
                    with open(target_file, "r", encoding="utf-8") as jf:
                        cdata = json.load(jf)
                    json_lid = str(cdata.get("lesson_id", "")).strip()
                    json_title = cdata.get("title", "").strip()
                    json_unit = cdata.get("unit", "").strip()

                    if json_lid != lid:
                        metadata_mismatches.append(
                            f"{target_file.name}: JSON lesson_id '{json_lid}' != syllabus id '{lid}'"
                        )
                    # Compare titles leniently (ignoring casing / punctuation)
                    clean_s_title = re.sub(r"[^a-zA-Z0-9]", "", s_les["title"]).lower()
                    clean_j_title = re.sub(r"[^a-zA-Z0-9]", "", json_title).lower()
                    if clean_s_title != clean_j_title:
                        metadata_mismatches.append(
                            f"{target_file.name}: JSON title '{json_title}' != syllabus '{s_les['title']}'"
                        )
                except Exception as e:
                    metadata_mismatches.append(f"{target_file.name}: JSON load error: {e}")

    print(f"\n--- Structure Check Results ---")
    print(f"File/Folder Structure Mismatches: {len(mismatches)}")
    for m in mismatches:
        print("  [FAIL]", m)

    print(f"\nMetadata / Title Mismatches: {len(metadata_mismatches)}")
    for mm in metadata_mismatches[:20]:
        print("  [WARN]", mm)
    if len(metadata_mismatches) > 20:
        print(f"  ... and {len(metadata_mismatches) - 20} more metadata mismatches.")

if __name__ == "__main__":
    check_structure()
