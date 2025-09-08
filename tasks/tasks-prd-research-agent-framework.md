# Tasks — Research Agent Framework (consolidation)

## File origin and layout (how we distinguish originals vs new/generated)

To avoid collisions with existing project sources and make generated artifacts easy to find, use a clear directory strategy:

- "Original / upstream files" (unchanged): keep these in their existing locations (for example, `src/deep_research_from_scratch/...`). We
  will reference these by their current paths in the task list.
- "Framework sources (new)": create a dedicated parent package for new code: `src/research_agent_framework/`. All new modules required by
  this PRD will live under this folder (for example `src/research_agent_framework/config.py`,
  `src/research_agent_framework/prompts/renderer.py`).
- "Generated / example artifacts": place generated example code, scaffolding, and disposable artifacts under
  `src/research_agent_framework/generated/` or `notebooks/generated/`. These can be safely regenerated and will be ignored by CI unless
  explicitly included.

Benefits:

- Clear separation between existing project code and the new framework work.
- Easy to add the new package to PYTHONPATH for notebooks/tests without editing original modules.
- Generated artifacts are isolated and easy to remove or re-generate.

## Relevant Files

- `src/research_agent_framework/config.py` - New Pydantic v2 `Settings` (pydantic-settings) for environment-driven configuration and logging
  overrides.
- `src/research_agent_framework/bootstrap.py` - `bootstrap()` that calls `environs.Env().read_env()`, installs `rich.traceback`, and
  configures `loguru`.
- `src/research_agent_framework/prompts/renderer.py` - Jinja2 `render_template(template_name: str, context: dict) -> str` using
  `StrictUndefined`.
- `src/research_agent_framework/prompts/templates/*.j2` - Directory for Jinja2 prompt templates referenced by logical names (see Notes below
  about sourcing templates from existing `prompts.py`).
- `src/research_agent_framework/models.py` - Pydantic v2 models: `Scope`, `ResearchTask`, `EvalResult`, `SerpResult` (with `raw: dict`).
- `src/research_agent_framework/llm/client.py` - `LLMClient` Protocol and `MockLLM` implementation for deterministic tests.
- `src/research_agent_framework/mcp/stub.py` - In-process async MCP stub for message passing in tests.
- `src/research_agent_framework/agents/base.py` - `Agent` Protocol and partial `ResearchAgent` implementation accepting typed `context`.
- `src/research_agent_framework/adapters/search/__init__.py` - Search adapter interface and conservative SerpAPI/Tavily adapters with
  `from_raw` factories.
- `tests/test_models.py` - Unit tests validating Pydantic models and edge cases (tests may refer to either `src/research_agent_framework` or
  existing modules when needed).
- `tests/test_renderer.py` - Unit tests for prompt rendering and StrictUndefined behavior.
- `tests/test_bootstrap.py` - Test ensuring `bootstrap()` reads env and configures logging without raising.
- `tests/test_integration_mock_stack.py` - Integration test wiring `MockLLM` + MCP stub demonstrating an agent flow.
- `notebooks/0_consolidated_research_agent.ipynb` - Demo notebook using the `src/research_agent_framework` package and mock stack.

### Notes

- Unit tests should use `pytest` and `pytest-asyncio`. Place tests in `tests/` alongside code where helpful.
- Base Jinja `.j2` templates will be derived from the existing `src/deep_research_from_scratch/prompts.py` (use its strings as a starting
  point). Templates will live under `src/research_agent_framework/prompts/templates/` and be referenced by logical name in the renderer
  helper.
- Tests and the consolidated notebook are living artifacts: update the notebook and relevant tests incrementally after completing each
  parent task, particularly after tasks that change public APIs (models, renderer, agents, adapters, bootstrap). Record which tests/notebook
  changes are required as subtasks for each parent task.

## Tasks

### Recommended priority order (short)

- Phase A (highest): Adapters (mock search), MockLLM tests, and small deterministic building blocks that other code depends on.
- Phase B: Agent Protocol and minimal `ResearchAgent` implementation (depends on Phase A for deterministic tests).
- Phase C: Supervisor robustness and error-policy work (depends on Phase A+B to exercise failure branches).
- Phase D: End-to-end integration test and notebooks/demos (run once A-C are in place).
- Note: MCP stub is anticipatory; implement only if needed for integration scenarios (lower priority).

- [x] 1. Create configuration and bootstrap
  - [x] 1.1 Add `src/research_agent_framework/config.py` with `Settings` using `pydantic-settings` and environment-driven fields.
     (implemented)
  - [x] 1.2 Add `src/research_agent_framework/bootstrap.py` with `bootstrap()` that reads `.env` via `environs`, installs `rich.traceback`,
     and configures `loguru`.
  - [x] 1.3 Add unit tests in `tests/test_bootstrap.py` verifying `bootstrap()` runs idempotently.
  - [x] 1.4 Record notebook/test updates required (notebook import path, environment bootstrap invocation).
    - Notebook cells for sys.path and bootstrap are present; tests for config/bootstrap pass. Ready for next phase.
  - [x] 1.5 Update notebook demo cells to explicitly import and use the deterministic `MockSearchAdapter` and `MockLLM` when available so
    demo cells are reproducible.

- [ ] 2. Models and validation
  - [x] 2.1 Implement `src/research_agent_framework/models.py` with Pydantic v2 models: `Scope`, `ResearchTask`, `EvalResult`, `SerpResult`.
  - [x] 2.2 Add `tests/test_models.py` covering happy path and invalid inputs.
  - [x] 2.3 Update notebook cells that construct model instances and tests that import models.

- [x] 3. Prompt renderer
  - [x] 3.1 Create `src/research_agent_framework/prompts/renderer.py` using Jinja2 `Environment` with `StrictUndefined` and a
    `render_template` helper.
  - [x] 3.2 Add example templates in `src/research_agent_framework/prompts/templates/` derived from
    `src/deep_research_from_scratch/prompts.py`.
  - [x] 3.3 Add `tests/test_renderer.py` to ensure missing variables raise errors and rendering succeeds with correct context.
  - [x] 3.4 Update notebook rendering examples and any tests that depend on template names/locations.

- [x] 4. LLM client and MockLLM
  - [x] 4.1 Create `src/research_agent_framework/llm/client.py` with an `LLMClient` Protocol (async `generate(prompt: str) -> str`) and
    `MockLLM`.
  - [x] 4.2 Add tests that use `MockLLM` for deterministic outputs.
  - [x] 4.3 Update integration examples in the notebook to import and use `MockLLM`.

- 4A. Property-Based and Edge Case Testing (PBT)

  - [x] 4A.1.1 Use Hypothesis to generate random valid/invalid data for Pydantic models (`Scope`, `ResearchTask`, `EvalResult`,
    `SerpResult`).
  - [x] 4A.1.2 Assert correct validation, error handling, and serialization/deserialization. [COMPLETE]
  - [x] 4A.1.3 Update `tests/test_models.py` with PBTs and edge-case coverage. [COMPLETE]

  - [x] 4A.2 Add property-based tests for prompt renderer
    - [x] 4A.2.1 Use Hypothesis to generate random context dictionaries and template names. [COMPLETE]
    - [x] 4A.2.2 Assert rendering succeeds or fails as expected (e.g., missing keys raise errors). [COMPLETE]
    - [x] 4A.2.3 Update `tests/test_renderer.py` with PBTs and edge-case coverage. [COMPLETE]

  - [x] 4A.3 Add property-based tests for LLM client
    - [x] 4A.3.1 Use Hypothesis to generate random prompts and configs for `MockLLM`. [COMPLETE]
    - [x] 4A.3.2 Assert output is always a string and errors are handled gracefully. [COMPLETE]
    - [x] 4A.3.3 Update `tests/test_llm_mock.py` with PBTs and edge-case coverage. [COMPLETE]

  - [x] 4A.4 Update notebook and test documentation
    - [x] 4A.4.1 Record notebook/test updates required after adding PBTs. [COMPLETE]
    - [x] 4A.4.2 Ensure all new tests pass before proceeding to agent implementation. [COMPLETE]
  - [ ] 5. Agents (implementation)
    - [x] 5.1 Create `src/research_agent_framework/agents/base.py` defining `Agent` Protocol and `ResearchAgent` implementation.
      - [x] 5.1.1 Implement `ResearchAgent` class with dependency injection for an LLM client and optional search adapter. (implemented)
      - [x] 5.1.2 Unit tests & PBTs added in `tests/test_research_agent.py`. (implemented)
      - [x] 5.1.3 Notebook demo cell added to `notebooks/0_consolidated_research_agent.ipynb` showing `plan()` and `run()`. (implemented)

    - [x] 5.2 Unit tests for agents (implemented in `tests/test_research_agent.py`).

    - [x] 5.3 Define `ScoringProtocol` (Protocol) in `src/research_agent_framework/agents/base.py` or a dedicated scoring module
      - [x] Accepts all relevant data for scoring (e.g., restaurant info, reviews, location, user preferences)
      - [x] Returns a score (float or structured result)
      - [x] Add at least one example scoring implementation and unit tests

    - [x] 5.4 Define a unified `Location` Pydantic model/interface in `src/research_agent_framework/models.py`
      - [x] Fields for address, lat/lon, name, etc.
      - [x] Ensure adapters (LLM, SerpAPI, Tavily) can return/consume this model (duck-typed acceptance implemented)
      - [x] Add unit tests for model validation and edge cases

    Relevant files modified/added for 5.4:
    - `src/research_agent_framework/models.py` - Added unified `Location` model, validators, `distance` unit handling, and raw payload
      preservation.
    - `tests/test_models_location.py` - Unit tests and Hypothesis property-based tests for `Location` behavior.
    - `notebooks/0_consolidated_research_agent.ipynb` - Notebook cells demonstrating `Location` usage, sampling-based checks, and demo
      checks (non-test assertions).
    - `pyproject.toml` - Added `pydantic-extra-types`, `pint`, and `hypothesis` in dev extras for developer/testing convenience.

    - [ ] 5.5 Supervisor robustness, logging, and configurable error policy
      - [x] 5.5.1 Replace `print(...)` debug in `src/deep_research_from_scratch/multi_agent_supervisor.py` with structured logging using the
        bootstrap-exported `logger`/`console` (implemented: `multi_agent_supervisor.py` updated to use `get_settings()` logger/console and explicit policy handling).
      - [ ] 5.5.2 Add a `Settings` or env-driven toggle for supervisor error policy with modes: `record_and_continue` (default),
        `fail_fast`, and `configurable` (explicit choice at runtime). Add unit tests for each policy branch.
      - [ ] 5.5.3 Add tests that simulate researcher exceptions and assert the supervisor returns a controlled `Command` update with
        recorded error info and that non-failing researchers still contribute their notes.

- [ ] 6. Adapters (e.g., search)

  - [ ] 6.1 Create `research_agent_framework/adapters/search/__init__.py` and modules
    - [ ] Define `class SearchAdapter(Protocol)` with `async def search(self, q: str, **kwargs) -> list[SerpResult]`.
    - [ ] Implement `MockSearchAdapter` for tests returning canned `SerpResult` objects.
  - [ ] Implement `MockSearchAdapter` for tests returning canned `SerpResult` objects.
  - [ ] Add a `from_raw` factory where applicable to preserve raw payloads in `SerpResult.raw`.
  - [ ] Add a deterministic `MockSearchAdapter` implementation under `src/research_agent_framework/adapters/search/mock_search.py` for use
    by integration tests and notebook demos.
    - [ ] Implement `TavilySearchAdapter` for test repeatability and compatibility with original notebooks.
    - [ ] Implement `SerpAPISearchAdapter` as the primary real-world adapter, supporting restaurant/event/activity search and scoring.
    - [ ] Ensure adapters support unified `Location` model for input/output.
    - [ ] Consider LangChain-compatible tools for extensibility (optional, based on future use cases).

  - [ ] 6.2 Tests
    - [ ] `tests/test_adapters.py` verifying all adapters return valid `SerpResult` and `from_raw` preserves raw payload.
    - [ ] Add edge-case and error handling tests for each adapter.
    - [x] Add `tests/test_mock_search.py` verifying `MockSearchAdapter` returns `SerpResult` objects and preserves `raw` payload.

      ```markdown
      # Tasks — Research Agent Framework (consolidation)

      This file has been updated to reflect the repository's current state (as of this change). The implementation evidence was collected from
      `src/research_agent_framework/` and `tests/` in the workspace. The checklist below marks implemented components and the remaining work.

      ## Implemented components (verified)

      - `src/research_agent_framework/config.py` — Pydantic v2 `Settings`, `get_settings()`, `get_console()` and `get_logger()` helpers.
      - `src/research_agent_framework/bootstrap.py` — idempotent `bootstrap()` that reads a `.env` (if present), installs `rich.traceback` and
        configures `loguru` to write to a `rich.Console` instance.
      - `src/research_agent_framework/prompts/renderer.py` and `prompts/templates/` — Jinja2 renderer using `StrictUndefined` and example templates
        (templates present under `prompts/templates/`).
      - `src/research_agent_framework/models.py` — Pydantic v2 models: `Scope`, `ResearchTask`, `EvalResult`, `SerpResult`, `Location`, and
        related helpers/validators (distance handling, coords normalization).
      - `src/research_agent_framework/llm/client.py` — `LLMClient` protocol and `MockLLM` implementation (supports `generate` and `generate_model`).
      - `src/research_agent_framework/adapters/search/` — `schema.py`, `base.py`, and `mock_search.py` present; `MockSearchAdapter` returns
        deterministic `SerpResult` objects and a `SerpReply` contract.
      - `src/research_agent_framework/agents/base.py` — `Agent` Protocol and a minimal `ResearchAgent` implementation (`plan()` and `run()`).
      - `src/research_agent_framework/mcp/stub.py` — in-process async `MCPStub` message bus for tests.
      - `src/research_agent_framework/logging.py` — LoggingProtocol and concrete loggers (`LoguruLogger`, `StdLogger`) used by `config.py`.
      - Notebooks/tests demonstrating integration: `notebooks/0_consolidated_research_agent.ipynb` and a set of tests under `tests/` (e.g.
        `test_bootstrap.py`, `test_models.py`, `test_renderer.py`, `test_llm_mock.py`, `test_mock_search.py`, `test_research_agent.py`,
        `test_end_to_end_flow.py`, `test_integration_mock_stack.py`).

      ## Checklist (current status)

      - [x] 1. Configuration & bootstrap
        - [x] 1.1 `src/research_agent_framework/config.py` (Settings) — implemented
        - [x] 1.2 `src/research_agent_framework/bootstrap.py` — implemented and idempotent
        - [x] 1.3 `tests/test_bootstrap.py` — present

      - [x] 2. Models & validation
        - [x] 2.1 `src/research_agent_framework/models.py` — implemented (Scope, ResearchTask, EvalResult, SerpResult, Location)
        - [x] 2.2 `tests/test_models.py` — present

      - [x] 3. Prompt renderer
        - [x] 3.1 `src/research_agent_framework/prompts/renderer.py` — implemented
        - [x] 3.2 templates under `src/research_agent_framework/prompts/templates/` — present
        - [x] 3.3 `tests/test_renderer.py` — present

      - [x] 4. LLM client & MockLLM
        - [x] 4.1 `src/research_agent_framework/llm/client.py` — `LLMClient` protocol and `MockLLM` implemented
        - [x] 4.2 tests for `MockLLM` — present (`tests/test_llm_mock.py`)

      - [x] 5. Agents
        - [x] 5.1 `src/research_agent_framework/agents/base.py` — `Agent` Protocol and `ResearchAgent` implemented
        - [x] 5.2 `tests/test_research_agent.py` — present
        - [ ] 5.3 `ScoringProtocol` and example scoring implementations — NOT implemented

      - [x] 6. Adapters (mock)
        - [x] 6.1 `src/research_agent_framework/adapters/search/mock_search.py` — `MockSearchAdapter` implemented
        - [x] 6.2 `src/research_agent_framework/adapters/search/schema.py` — `SerpRequest` / `SerpReply` models present
        - [ ] 6.3 Real-world adapters (`SerpAPI`, `Tavily`) and `from_raw` factories — NOT implemented

      - [x] 7. MCP & integration test harness
        - [x] 7.1 `src/research_agent_framework/mcp/stub.py` — implemented
        - [x] 7.2 Integration tests demonstrating wired `MockLLM` + `MCPStub` + agent flow — present

      - [ ] 8. Supervisor robustness & error-policy
        - [ ] 8.1 Replace `print()` debug output in `src/deep_research_from_scratch/multi_agent_supervisor.py` with structured logging
          via the framework `get_settings()`/`console`/`logger` (partial edits exist elsewhere but the supervisor file still requires review)
        - [ ] 8.2 Add Settings-driven supervisor error policy modes (`record_and_continue`, `fail_fast`, `configurable`) with tests — NOT implemented

      - [ ] 9. Documentation & final test gating
        - [ ] 9.1 Run full test suite and fix any failing tests (recommended as a CI gate)
        - [ ] 9.2 Update `README.md` with exact run instructions for notebooks/tests and PYTHONPATH guidance

      ## Next recommended steps (short)

      1. Add a `ScoringProtocol` and at least one example scoring implementation with unit tests (helps close the agent feature gap).
      2. Implement `from_raw` factories or adapter helpers to preserve provider raw payloads consistently across adapters.
      3. Replace remaining raw `print()` uses (notebooks and `src/deep_research_from_scratch/*`) with `get_console()` / `get_logger()` usage and add supervisor error-policy toggles in `Settings` with tests.
      4. Run the full test suite locally (`pytest -q`) and address any remaining failures as CI gating.

      ## How this mapping was created

      I verified the presence and content of the files under `src/research_agent_framework/` and a representative set of tests under `tests/` before marking items implemented. The checklist focuses on concrete file-level evidence; implementation completeness (API surface, docstrings, edge-case coverage) may still require follow-up as noted above.

      ```
