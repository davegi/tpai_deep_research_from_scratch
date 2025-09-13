import json
import subprocess
import sys
from pathlib import Path

NB = Path(r"d:\repos\tpai_deep_research_from_scratch\notebooks\research_workflow_comprehensive.ipynb")
nb = json.loads(NB.read_text(encoding='utf-8'))

# Extract first N code cells
N = 6
code_cells = [c for c in nb['cells'] if c['cell_type']=='code'][:N]

# Build a temporary Python script that executes those cells sequentially
tmp = Path('tmp_run_cells.py')
with tmp.open('w', encoding='utf-8') as f:
    f.write('# Auto-generated runner for first {} code cells\n'.format(N))
    f.write('from pathlib import Path\n')
    f.write('import sys, os, asyncio\n')
    f.write('\n')
    f.write('# Preamble: ensure local src path is on sys.path before imports\n')
    f.write("repo_cwd=Path.cwd().resolve()\n")
    f.write("found_root=None\n")
    f.write("for candidate in [repo_cwd]+list(repo_cwd.parents):\n")
    f.write("    if (candidate/'src'/'research_agent_framework').exists() or (candidate/'research_agent_framework').exists():\n")
    f.write("        found_root=candidate.resolve();break\n")
    f.write("if found_root is not None:\n")
    f.write("    src_candidate=(found_root/'src') if (found_root/'src'/'research_agent_framework').exists() else found_root\n")
    f.write("    src_path=str(src_candidate)\n")
    f.write("    if src_path not in sys.path:\n")
    f.write("        sys.path.insert(0,src_path)\n")
    f.write("        os.environ['PYTHONPATH']=os.environ.get('PYTHONPATH','') or src_path\n")
    f.write("# End preamble\n\n")
    # write each cell code
    for i, cell in enumerate(code_cells, start=1):
        f.write('\n# ---- Cell {} ----\n'.format(i))
        for line in cell['source']:
            # keep lines as-is
            f.write(line + '\n')

print('Wrote', tmp)

# Run the script and capture output
proc = subprocess.run([sys.executable, str(tmp)], capture_output=True, text=True)
print('RETURN CODE:', proc.returncode)
print('STDOUT:\n', proc.stdout)
print('STDERR:\n', proc.stderr)

# cleanup
try:
    tmp.unlink()
except Exception:
    pass
