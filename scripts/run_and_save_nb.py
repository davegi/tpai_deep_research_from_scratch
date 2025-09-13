"""Run a notebook using nbclient and save the executed copy.

Usage: python scripts/run_and_save_nb.py <input-ipynb> <output-ipynb>
"""
import sys
from pathlib import Path

from nbformat import read, write, NO_CONVERT
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


def run_notebook(src: Path, dst: Path, timeout=600):
    nb = read(str(src), as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name='python3')
    try:
        client.execute()
    except CellExecutionError as e:
        print('CellExecutionError:', e)
        # still try to write partial output
    write(nb, str(dst))


def main(argv):
    if len(argv) < 3:
        print('Usage: run_and_save_nb.py <input.ipynb> <output.ipynb>')
        return 2
    src = Path(argv[1]).resolve()
    dst = Path(argv[2]).resolve()
    print('Running', src)
    run_notebook(src, dst)
    print('Saved executed notebook to', dst)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
