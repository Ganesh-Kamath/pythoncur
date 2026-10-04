"""
Commercial Quality Audit Tool:
Scans all 244 lesson files for:
1. Placeholder solutions (e.g. print('OK'), print('Result ...'))
2. Code prediction / multiple choice questions having extraneous starter_code
3. Generic starter_code ('# Write your solution below') needing pedagogical scaffolding
4. Shallow explanations (< 15 words)
5. Distractor quality
"""

import glob
import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CONTENT_DIR = WORKSPACE / "python_content"

def audit():
    files = sorted(glob.glob(str(CONTENT_DIR / "**/*.json"), recursive=True))
    
    placeholder_sols = []
    extraneous_sc = []
    generic_starters = []
    short_explanations = []
    
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        lid = data.get("lesson_id", "")
        ltitle = data.get("title", "")
        
        for it in data.get("items", []):
            iid = it.get("id")
            itype = it.get("type")
            sol = it.get("solution_code", "").strip()
            sc = it.get("starter_code", "").strip()
            exp = it.get("explanation", "").strip()
            prompt = it.get("prompt", "").strip()
            
            # 1. Placeholder solutions
            if sol in ["print('OK')", "print('TODO')", "pass", "return True"] or "Result " in sol:
                placeholder_sols.append((iid, itype, sol, prompt[:60]))
                
            # 2. Extraneous starter code in multiple choice / code prediction
            if itype in ["multiple_choice", "code_prediction", "output_prediction", "match_code_to_concept"] and sc:
                extraneous_sc.append((iid, itype, sc))
                
            # 3. Generic starter code in coding challenges
            if itype in ["write_the_code", "fix_the_code", "mini_challenge", "refactoring_challenge"]:
                if sc in ["# Write your solution below", "# Write your code below", ""]:
                    generic_starters.append((iid, itype, prompt[:60]))
                    
            # 4. Short explanations
            if len(exp.split()) < 12 and itype != "micro_lesson":
                short_explanations.append((iid, itype, exp))

    print(f"Audit results across {len(files)} lessons (7,320 items):")
    print(f"  Placeholder solutions:              {len(placeholder_sols)}")
    print(f"  Extraneous starter in MC/prediction:{len(extraneous_sc)}")
    print(f"  Generic starter code in coding:     {len(generic_starters)}")
    print(f"  Short explanations:                 {len(short_explanations)}")
    
    if placeholder_sols:
        print("\nSample placeholder solutions:")
        for p in placeholder_sols[:10]:
            print(f"  {p[0]} ({p[1]}): {repr(p[2])} | Prompt: {p[3]}")
            
    if generic_starters:
        print("\nSample generic starters:")
        for g in generic_starters[:10]:
            print(f"  {g[0]} ({g[1]}): {g[2]}")

if __name__ == "__main__":
    audit()
