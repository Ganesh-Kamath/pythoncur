import glob

units_to_list = ["unit_03", "unit_04", "unit_05", "unit_07", "unit_10", "unit_24", "unit_34", "unit_37"]
for u in units_to_list:
    files = sorted(glob.glob(f"python_content/{u}/*.json"))
    print(f"=== {u} ===")
    for f in files:
        print(" ", f.split("\\")[-1].split("/")[-1])
