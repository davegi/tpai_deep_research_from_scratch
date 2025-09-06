# Helpers and small debug scripts

Files:

- `import_check.py` — quick smoke test to ensure core demo classes import correctly.
- `run_demo.py` — small deterministic demo exercising `MockLLM` and `MockSearchAdapter`.
- `debug_bootstrap_subprocess.py` — helper that runs bootstrap in an isolated subprocess and prints results.

Usage (Windows cmd, using the repository virtualenv):

``` bash
d:\repos\tpai_deep_research_from_scratch\.venv\Scripts\python.exe scripts\import_check.py
d:\repos\tpai_deep_research_from_scratch\.venv\Scripts\python.exe scripts\run_demo.py
d:\repos\tpai_deep_research_from_scratch\.venv\Scripts\python.exe scripts\debug_bootstrap_subprocess.py
```

If you'd like these to be part of CI or made into proper test fixtures, I can help convert them.
