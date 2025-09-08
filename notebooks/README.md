# Notebooks helper files

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
