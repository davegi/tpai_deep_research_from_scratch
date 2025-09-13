import json
from pathlib import Path
import uuid

p = Path(r"d:\repos\tpai_deep_research_from_scratch\notebooks\research_workflow_comprehensive.ipynb")
nb = json.loads(p.read_text(encoding='utf-8'))
changed = 0
for i, c in enumerate(nb.get('cells', []), start=1):
    md = c.get('metadata')
    if md is None:
        md = {}
    if 'id' not in md:
        md['id'] = f"#VSC-auto-{i}-{uuid.uuid4().hex[:8]}"
        c['metadata'] = md
        changed += 1

p.write_text(json.dumps(nb, ensure_ascii=False, indent=4), encoding='utf-8')
print(f'added id to {changed} cells')
