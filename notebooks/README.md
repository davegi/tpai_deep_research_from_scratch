# Notebook helper and recommended usage

===================================

This folder contains educational notebooks for the project and a small helper
`nb_bootstrap.py` used to ensure local `src` is on `sys.path` and to run the
project's `bootstrap()` function from notebooks.

## Usage

At the top of your notebook, add (file-based loader — works whether or not `notebooks` is a package):

```python
import importlib.util
from pathlib import Path
helper_path = Path(__file__).parent / 'nb_bootstrap.py'
spec = importlib.util.spec_from_file_location('nb_bootstrap', str(helper_path))
if spec is None or spec.loader is None:
    raise ImportError(f'Failed to load nb_bootstrap from {helper_path!s}: spec or loader is None')
nb_bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nb_bootstrap)
settings, console, logger = nb_bootstrap.ensure_src_and_bootstrap()
```

This keeps notebooks DRY and avoids repeating path insertion logic across multiple
cells.

## Long-term recommendation

For an even more robust environment, install the package in editable mode from
the repository root:

```bash
pip install -e .
```

That removes the need for path hacks in notebooks while developing.

## Notebooks helper files

This folder contains runnable demo notebooks and helpers used by the demo workflow.

notebook_head.json

- Purpose: a canonical notebook "head" used when programmatically creating or seeding new notebooks. It contains a small set of bootstrap cells (sys.path fix, demo imports, and bootstrap invocation) that other notebooks can reuse.
- Current usage: There are no direct code references to `notebook_head.json` in the repository (it's a convenience/template file). It is safe to keep in the repository for manual reuse or as a template for generating notebooks.

Recommended next actions

- Keep (default): leave `notebook_head.json` where it is. It is harmless and useful as a template for new notebooks.
- Move: if you prefer generated artifacts to live under a dedicated folder, move it to `notebooks/generated/notebook_head.json` with:

```cmd
mkdir "notebooks\generated"
move "notebook_head.json" "notebooks\generated\notebook_head.json"
```

- Delete: if you are sure it's not needed, delete it with:

```cmd
del "notebook_head.json"
```

If you'd like, I can move or delete the file now—tell me which action you prefer and I'll apply it.
