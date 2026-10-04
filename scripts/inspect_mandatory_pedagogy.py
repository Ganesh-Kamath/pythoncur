import json
import glob
from pathlib import Path

def inspect():
    root = Path("python_content")
    lessons = sorted(list(root.glob("unit_*/*.json")))
    print(f"Total lesson files found: {len(lessons)}")
    
    # We want to check how well the mandatory changes are represented:
    # 1. Variables as references / aliasing / mutability
    # 2. == vs is
    # 3. None / truthiness
    # 4. return vs print
    # 5. Real bugs in spot_the_bug / fix_the_code
    # 6. SQL injection / parameterized queries
    # 7. AsyncIO blocking vs non-blocking
    # 8. Composition vs inheritance
    
    topics = {
        "aliasing_mutation": 0,
        "is_vs_equal": 0,
        "truthiness": 0,
        "return_vs_print": 0,
        "parameterized_queries": 0,
        "async_event_loop": 0,
        "composition_over_inheritance": 0,
        "type_hints": 0
    }
    
    for lp in lessons:
        with open(lp, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data.get("items", []):
            text = (str(item.get("question", "")) + " " +
                    str(item.get("explanation", "")) + " " +
                    str(item.get("prompt", "")) + " " +
                    str(item.get("content", "")) + " " +
                    str(item.get("code", ""))).lower()
            
            if "alias" in text or "mutation" in text or "mutability" in text:
                topics["aliasing_mutation"] += 1
            if "==" in text and " is " in text:
                topics["is_vs_equal"] += 1
            if "truthy" in text or "falsy" in text or "truthiness" in text:
                topics["truthiness"] += 1
            if "return" in text and "print" in text:
                topics["return_vs_print"] += 1
            if "parameterized" in text or "injection" in text:
                topics["parameterized_queries"] += 1
            if "asyncio" in text or "event loop" in text:
                topics["async_event_loop"] += 1
            if "composition" in text and "inheritance" in text:
                topics["composition_over_inheritance"] += 1
            if "->" in text or ": int" in text or ": str" in text or "type hint" in text:
                topics["type_hints"] += 1
                
    print("Pedagogical topic distribution across items:")
    for k, v in topics.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    inspect()
