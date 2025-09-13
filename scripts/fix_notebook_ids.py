import json
from pathlib import Path
p = Path(r"d:\repos\tpai_deep_research_from_scratch\notebooks\research_workflow_comprehensive.ipynb")
nb = json.loads(p.read_text(encoding='utf-8'))
# Ensure nbformat fields
if 'nbformat' not in nb:
    nb['nbformat'] = 4
if 'nbformat_minor' not in nb:
    nb['nbformat_minor'] = 5
if 'metadata' not in nb:
    nb['metadata'] = {}

changed = 0
for c in nb.get('cells', []):
    if 'id' in c:
        md = c.get('metadata') or {}
        md['id'] = c.pop('id')
        c['metadata'] = md
        changed += 1

p.write_text(json.dumps(nb, ensure_ascii=False, indent=4), encoding='utf-8')
print(f'fixed {changed} cells and wrote notebook')
