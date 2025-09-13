import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
nb_paths = [
    REPO_ROOT / 'notebooks' / 'research_workflow_comprehensive.ipynb',
    REPO_ROOT / 'notebooks' / '0_consolidated_research_agent.ipynb',
]

for p in nb_paths:
    print(f"Executing notebook: {p}")
    nb = nbformat.read(str(p), as_version=4)
    client = NotebookClient(nb, timeout=600, kernel_name='python3')
    try:
        client.execute()
    except CellExecutionError as e:
        print(f"Execution failed for {p}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error executing {p}: {e}")
        raise
    out_path = p.with_name(p.stem + '.executed.ipynb')
    nbformat.write(nb, str(out_path))
    print(f"Wrote executed notebook: {out_path}")

print('All notebooks executed successfully.')
