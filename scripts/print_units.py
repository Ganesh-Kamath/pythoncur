import json

with open('manifest.json', 'r', encoding='utf-8') as f:
    m = json.load(f)

print("Keys of unit:", m['units'][0].keys())
for u in m['units']:
    uid = u.get('id') or u.get('unit_id')
    title = u.get('title')
    lessons = u.get('lessons', [])
    print(f"Unit {uid}: {title} ({len(lessons)} lessons)")
