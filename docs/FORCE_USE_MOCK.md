FORCE_USE_MOCK
=================

Purpose
-------

`FORCE_USE_MOCK` is a simple environment toggle used by the educational notebook and
helper utilities to force deterministic, mock-based behavior for adapters and LLMs.

When set to a truthy value (`1`, `true`, `yes`) the framework will prefer mock
implementations even if credentials or real provider names are present. This is
useful for reproducible demos, CI runs, and contributor development where live
API calls must be avoided.

How it works
------------

- `research_agent_framework.helpers.switchboard.use_mock_search()` and
  `use_mock_llm()` check `FORCE_USE_MOCK` first and return `True` when set.
- Adapter factories (e.g., `from_raw_adapter`) and `llm_factory` are used by
  notebook cells and examples; code paths in the notebook honor these helper
  decisions to pick mock implementations.

Recommended usage
-----------------

In notebooks or local runs you can set the env var to force deterministic runs:

```bash
export FORCE_USE_MOCK=1   # POSIX shells
set FORCE_USE_MOCK=1      # Windows cmd
```

Unset it to return to normal behavior.
