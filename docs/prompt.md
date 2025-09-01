# Project Summary — consolidation plan for notebooks and codebase

This file summarizes the conversation (project brainstorming session) captured in `docs/chat_history.md` and records the decisions, deltas,
constraints, planned implementation order, open questions, and next steps for consolidating the notebooks into a single, well-structured
project.

## High-level goal

Consolidate five notebooks (scoping, research agents, MCP variants, supervisor, full agent) into a single, well-documented, testable
implementation and a consolidated notebook that demonstrates the full flow. Extract prompt templates to Jinja, use Pydantic v2 for models
and BaseSettings, prefer LangGraph/ LangChain MCP primitives when available, and provide a skeleton of source files, tests, and CLI glue for
easy conversion from notebook to scripts.

## Key decisions and requirements

- Python 3.12+
- Stable, state-of-the art PKGs
- Load environment variables before most imports. Use `environs` (confirmed) to populate `os.environ` early in notebook top-cell and scripts
  so libraries that read env on import behave correctly.
- Use Jinja2 for all prompts (templates as `.j2`) and configure `StrictUndefined` to catch missing variables.
- Use Pydantic v2 and `pydantic-settings` (BaseSettings) for configuration. Avoid Pydantic v1.
- Prefer `LangGraph`/`LangChain` MCP client/server primitives when present in the environment; provide an in-process async stub for
  deterministic tests and notebooks.
- Agents must accept a typed `context` parameter (holds config, logger/console, clients) to avoid module-level globals and to support
  different UIs (notebook, CLI, mobile, browser). Use Protocols for interfaces and TypedDict for mutable agent-state where appropriate.
- CLI glue: use CyclOpts as requested for minimal CLI entrypoints. CLI is optional but useful for converting notebooks to scripts.
- Testing: use `pytest`, `pytest-asyncio`, `hypothesis`, and `faker` (for synthetic data). Use MockLLM and in-process MCP stub to keep tests
  deterministic.
- Logging: default to `loguru` (configurable). Install `rich.traceback` in bootstrap for readable tracebacks in notebooks.
- Keep rich usage tasteful and educational (color/verbosity ok), but avoid excessive UI complexity.
- Preserve and extract evaluator logic (from scoping notebook) into `src/evals.py`. Render evaluator prompts via Jinja and test via mocks.

## Additional Thoughts

- Enforce early env bootstrap using `environs.Env().read_env()` at the very top of notebooks / script entrypoints.
- Use `environs` rather than `python-dotenv` per the user's confirmation.
- Confirmed CyclOpts as the CLI library.
- Agents accept `context` objects; no global console or logger references.
- LangGraph MCP primitives are preferred and will be detected at runtime; fall back to in-process stub if not available.
- SerpAPI: add typed adapter and Pydantic models; start conservative and store raw fields for unknown complex nested fields.
- File origin marking: files that were originally created by notebook `%writefile` will be named with a `_from_notebook__{nb}__{module}.py`
  prefix to make provenance clear.

## Planned file-generation sequence (order of implementation)

- Ensure that files - of any type/extension - are either isolated in new folders, or use a naming convention that differentiates between
  current/existing/starting files in the project and those you create

1. `src/config.py` — Pydantic v2 BaseSettings-backed configuration.
2. `src/bootstrap.py` — early env load (environs), `rich.traceback.install()`, log setup.
3. `src/prompts/**` — Jinja2 template directory and a prompt renderer with StrictUndefined.
4. `src/protocols.py` — Protocols for Agent/LLM/MCP/Tool interfaces.
5. `src/models.py` — Pydantic models (Scope, ResearchTask, EvalResult, SerpAPI models, MCPMessage) and TypedDicts for mutable agent-state.
6. `src/llm/client.py` — LLM client abstraction and `MockLLM` for tests; add instrumentation hooks.
7. `src/agents/` — Agent base classes and `InProcessAgent` and `research_agent_full` superset implementation.
8. `src/mcp/` — LangGraph adapter wiring and an in-process MCP stub for testing.
9. `src/tools/serpapi.py` — SerpAPI adapter and sample Pydantic response models.
10. `tests/` — Pytest unit tests, Hypothesis PBTs, fixtures, and faker-based fixtures. Include tests for prompt rendering, model validation,
    agent flows with MockLLM, and MCP stub interactions.
11. `scripts/` — Minimal CyclOpts CLI scripts, e.g., `run_demo.py`, optional `start_mcp_server.py` only if LangGraph adapters are
    insufficient.
12. `notebooks/0_consolidated_research_agent.ipynb` — Notebook that imports from `src/` and demonstrates the entire flow.

## Naming / provenance convention

- Files generated originally from notebook `%writefile` will be identifiable with the `_from_notebook__{nb}__{module}.py` prefix in `src/`
  to make it easy to trace origin and facilitate debugging.

## SerpAPI modeling approach (conceptual)

- Start with small, well-typed Pydantic models for the key SERP response subsets (search result items, location summary, event summary).
  Keep a `raw: dict` fallback to store unmodeled fields.
- Provide `from_serp_raw(raw: dict)` factory methods to normalize inputs and to ease testing via sample JSON fixtures.

## Testing strategy highlights

- Unit tests for models, prompt rendering (StrictUndefined behavior), small pure functions.
- Integration tests using `MockLLM` and an in-process MCP stub (async queue). No live external calls in CI; SerpAPI and LLM providers
  mocked. Real-key runs allowed locally with `.env`.
- Property tests with Hypothesis for invariants (e.g., scope -> tasks mapping).
- Use `faker` for realistic fixture data where appropriate.

## Reply to create-prd

1. b
2. a, c, d: software developer implementing the project - including UTs and PBTs
3. d
4. 1-3
5. already specified or infer from context
6. yes. flow, c4, architecture diagrams, etc.
7. asap, 1, 2, 3, 5, 9, 10 (pytest (UTs) first), 12 (based on the 'current' iterations feature requirement)
8. i prefer longer - w/in reason - descriptive names, use std. Pythonic naming/style conventions
9. no, but considering the project's goals of being educational and an environment for experimentation, `assertpy.assert_that()` w/comprehensive comparators and descriptive description statements in the code are acceptable
10. again, remember the goal and stay strictly w/scope. do not expand the feature set w/out my confirmation. if in doubt, be conservative and/or ask for my help
