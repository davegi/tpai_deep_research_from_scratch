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

- [x] 1. Create configuration and bootstrap
  - [x] 1.1 Add `src/research_agent_framework/config.py` with `Settings` using `pydantic-settings` and environment-driven fields.
     (implemented)
  - [x] 1.2 Add `src/research_agent_framework/bootstrap.py` with `bootstrap()` that reads `.env` via `environs`, installs `rich.traceback`,
     and configures `loguru`.
  - [x] 1.3 Add unit tests in `tests/test_bootstrap.py` verifying `bootstrap()` runs idempotently.
  - [x] 1.4 Record notebook/test updates required (notebook import path, environment bootstrap invocation).
    - Notebook cells for sys.path and bootstrap are present; tests for config/bootstrap pass. Ready for next phase.

- [ ] 2. Models and validation
  - [x] 2.1 Implement `src/research_agent_framework/models.py` with Pydantic v2 models: `Scope`, `ResearchTask`, `EvalResult`, `SerpResult`.
  - [x] 2.2 Add `tests/test_models.py` covering happy path and invalid inputs.
  - [ ] 2.3 Update notebook cells that construct model instances and tests that import models.

- [ ] 3. Prompt renderer
  - [ ] 3.1 Create `src/research_agent_framework/prompts/renderer.py` using Jinja2 `Environment` with `StrictUndefined` and a
    `render_template` helper.
  - [ ] 3.2 Add example templates in `src/research_agent_framework/prompts/templates/` derived from
    `src/deep_research_from_scratch/prompts.py`.
  - [ ] 3.3 Add `tests/test_renderer.py` to ensure missing variables raise errors and rendering succeeds with correct context.
  - [ ] 3.4 Update notebook rendering examples and any tests that depend on template names/locations.

- [ ] 4. LLM client and MockLLM
  - [ ] 4.1 Create `src/research_agent_framework/llm/client.py` with an `LLMClient` Protocol (async `generate(prompt: str) -> str`) and
    `MockLLM`.
  - [ ] 4.2 Add tests that use `MockLLM` for deterministic outputs.
  - [ ] 4.3 Update integration examples in the notebook to import and use `MockLLM`.
- [ ] 5. Agents
  - [ ] 5.1 Create `src/research_agent_framework/agents/base.py` defining `Agent` Protocol and `ResearchAgent` partial impl that accepts
    typed `context`.

  - [ ] 5.2 Unit tests for agents
    - [ ] Add `tests/test_research_agent.py` (pytest-asyncio):
      - [ ] Test `plan` uses templates and returns plausible `ResearchTask` list
      - [ ] Test `run` with `MockLLM` returns `EvalResult` instances

- [ ] 6. Adapters (e.g., search)
  - [ ] 6.1 Create `research_agent_framework/adapters/search/__init__.py` and modules
    - Define `class SearchAdapter(Protocol)` with `async def search(self, q: str, **kwargs) -> list[SerpResult]`.
    - Provide `class MockSearchAdapter(SearchAdapter)` for tests returning canned `SerpResult` objects.

  - [ ] 6.2 Tests
    - `tests/test_adapters.py` verifying `MockSearchAdapter` returns `SerpResult` and `from_raw` preserves raw payload.

  - [ ] 6.3 Notebook updates
    - Add demo cell that uses `MockSearchAdapter` and shows how results are used by the agent.

- [ ] 7. Notebook and demo (living artifact)
  - [ ] 7.1 Create `notebooks/0_consolidated_research_agent.ipynb` (skeleton)
    - Top cells: `sys.path` fix, `bootstrap()` call, import `ResearchAgent`, `MockLLM`, `MockSearchAdapter`.
    - Sequential cells: demonstrate models → renderer → agent plan → agent run (with MockLLM) → show EvalResults

  - [ ] 7.2 Per-task iterative updates
    - After each parent task is completed, add/adjust notebook cells that demonstrate the newly implemented capability (e.g., after models:
      show model instance; after renderer: render example template).
    - Mark notebook cells with comments like `# TASK-3: renderer example` so reviewers and CI can map features to cells.

  - [ ] 7.3 Per-task test targets
    - Create `scripts/run_tests_for_task.py` which accepts a task id or module pattern and runs the subset of tests relevant to that task
      (helps enforce "ALL tests pass before moving on").

- [ ] 8. MCP stub
  - [ ] 8.1 Implement `research_agent_framework/mcp/stub.py`
    - Provide an in-process async message bus with `register_handler(topic, handler)` where `handler` is an async callable, and `async def
      publish(topic, message)`.
    - Keep the API small and fully testable without external network calls.

  - [ ] 8.2 Integration test
    - `tests/test_integration_mock_stack.py`:
      - Wire `ResearchAgent` + `MockLLM` + `MCPStub` and assert a multi-step exchange produces expected `EvalResult` objects.

- [ ] 9. Finalize tests and docs
  - [ ] 9.1 Run full test suite locally and fix any failures (unit + integration where fast). Provide a short test report in `tasks/`.
  - [ ] 9.2 Update `README.md` with exact run instructions for the notebook and tests and commit changes; include tips for adding the repo
    root to PYTHONPATH in notebooks.

### Relevant Files (detailed mapping)

- `research_agent_framework/config.py` — Settings + logging config
- `research_agent_framework/bootstrap.py` — bootstrap() helper
- `research_agent_framework/models.py` — Scope, ResearchTask, EvalResult, SerpResult
- `research_agent_framework/prompts/renderer.py` — render_template helper
- `research_agent_framework/prompts/templates/*.j2` — derived templates from `src/deep_research_from_scratch/prompts.py`
- `research_agent_framework/llm/client.py` — LLMClient protocol and MockLLM
- `research_agent_framework/agents/base.py` — Agent protocol and ResearchAgent implementation
- `research_agent_framework/adapters/search/*` — Search adapter interface + MockSearchAdapter
- `research_agent_framework/mcp/stub.py` — lightweight in-process MCP stub
- `notebooks/0_consolidated_research_agent.ipynb` — demo notebook (skeleton + per-task cells)
- `tests/test_config.py`, `tests/test_bootstrap.py`, `tests/test_models.py`, `tests/test_renderer.py`, `tests/test_llm_mock.py`,
  `tests/test_research_agent.py`, `tests/test_adapters.py`, `tests/test_integration_mock_stack.py`

### Notes on testing strategy and gating

- Primary tests ui is VS Code's Test Explorer. In addition...
  - Enforce the rule: "ALL existing and newly added tests  must pass before merging or proceeding to the next parent task." Use
    `scripts/run_tests_for_task.py` to run focused test subsets during development.
  - Prefer small, fast unit tests. Keep integration tests optional for CI but runnable locally.
  - Use `pytest -k <pattern>` and `pytest-asyncio` for async tests; include examples in `README.md`.
