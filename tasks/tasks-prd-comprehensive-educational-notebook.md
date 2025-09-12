# Task List for Comprehensive Educational Notebook PRD

## Relevant Files

- `notebooks/research_workflow_comprehensive.ipynb` - Primary educational notebook to build per PRD.
- `tasks/prd-comprehensive-educational-notebook.md` - Source PRD for requirements and scope.
- `src/research_agent_framework/bootstrap.py` - Bootstrap entrypoint; environment and logging setup.
- `src/research_agent_framework/config.py` - Settings, console, and logger helpers used by notebook.
- `src/research_agent_framework/logging.py` - Structured logging utilities.
- `src/research_agent_framework/llm/client.py` - LLM factory and `MockLLM`; toggles between providers.
- `src/research_agent_framework/agents/base.py` - Base agent constructs referenced in demos.
- `src/research_agent_framework/agents/scoring.py` - Scoring helpers for analysis sections.
- `src/research_agent_framework/adapters/search/__init__.py` - Search adapter factory by provider.
- `src/research_agent_framework/adapters/search/mock_search.py` - Deterministic mock search adapter.
- `src/research_agent_framework/adapters/search/serpapi_search.py` - SerpAPI adapter (stubbed/live-ready).
- `src/research_agent_framework/adapters/search/tavily_search.py` - Tavily adapter (stubbed/live-ready).
- `src/research_agent_framework/prompts/templates/research_agent_prompt.j2` - Core research agent prompt template.
- `src/research_agent_framework/prompts/templates/clarify_with_user_instructions.j2` - Clarification prompt template.
- `src/deep_research_from_scratch/research_agent.py` - Example agent orchestration used for demos.
- `src/deep_research_from_scratch/research_agent_scope.py` - Scoping workflow components.
- `src/deep_research_from_scratch/research_agent_full.py` - Full workflow example logic.
- `src/deep_research_from_scratch/multi_agent_supervisor.py` - Multi-agent coordination demo logic.
- `src/deep_research_from_scratch/state_research.py` - Research state models.
- `src/deep_research_from_scratch/state_scope.py` - Scope state models.
- `tests/test_end_to_end_flow.py` - End-to-end tests to mirror in notebook.
- `tests/test_research_agent.py` - Research agent behavior; sync notebook examples.
- `tests/test_renderer.py` and `tests/test_renderer_rich*.txt` - Rich output expectations.
- `tests/test_serpapi_and_tavily_adapters.py` - Search adapters parity; use for deterministic examples.
- `tests/test_llm_mock.py` - MockLLM behavior; leverage for deterministic outputs.
- `tests/test_supervisor_policy*.py` - Supervisor demos; align multi-agent examples.

### Notes

- This repository uses pytest. Run tests with: `pytest -q` or a specific test: `pytest tests/test_research_agent.py::test_run_uses_mockllm
  -q`.
- Prefer deterministic examples using mocks by default; clearly label optional live-provider sections and guard with env vars.
- Keep notebook code Pylance/flake8 clean; treat warnings as actionable for the educational audience.

## Tasks

- [x] 1.0 Outline notebook structure and section plan (PRD-aligned)
  - [x] 1.1 Draft top-level sections and learning objectives
  - [x] 1.2 Insert TODO anchors per section and cross-link to tests
  - [x] 1.3 Add brief overview of architecture and technologies used

- [x] 2.0 Add Mermaid architecture and data flow diagrams
  - [x] 2.1 Component diagram: agents, LLM client, adapters, state, logging
  - [x] 2.2 Sequence diagram: user → scoping → research → synthesis → report
  - [x] 2.3 Data model diagram: key models and relationships

  - [x] 3.0 Implement environment bootstrap and configuration walkthrough
    - [x] 3.1 Show bootstrap invocation and rich console output
    - [x] 3.2 Display resolved settings and notable defaults
    - [x] 3.3 Explain configuration impact on behavior and logging (notebook includes settings table, explanatory text, and a safe reload
      demo)

- [x] 5.0 Set up LLM clients with options and toggles
  - [x] 5.1 Present `llm_factory` usage and provider selection
  - [x] 5.2 Demonstrate `MockLLM` deterministic behavior
  - [x] 5.3 Expose temperature/max_tokens and document their impact

- [ ] 6.0 Add mock/live provider toggles and deterministic fallbacks
- [x] 6.0 Add mock/live provider toggles and deterministic fallbacks
  - [x] 6.1 Implement env-based switches for LLM and search adapters
  - [x] 6.2 Default to mocks; clearly label live-call cells
  - [x] 6.3 Include a single "switchboard" helper cell to centralize toggles

- [x] 7.0 Implement user clarification and scoping demo
  - [x] 7.2 Show iterative refinement using deterministic responses
  - [x] 7.3 Capture scope state object and validation

- [x] 8.0 Generate research brief aligned with tests
  - [x] 8.1 Produce brief using the same models/fixtures as tests
  - [x] 8.2 Validate brief fields with assertpy
  - [x] 8.3 Render brief with rich output consistent with test snapshots

- [ ] 9.0 Implement multi-agent coordination workflow demo
  - [ ] 9.1 Demonstrate supervisor policy with deterministic steps
  - [ ] 9.2 Log agent messages and state transitions
  - [ ] 9.3 Align with `test_supervisor_policy*.py` expectations

- [ ] 10.0 Add research compression and synthesis section
  - [ ] 10.1 Show compression strategy with MockLLM
  - [ ] 10.2 Synthesize findings into structured objects
  - [ ] 10.3 Validate synthesized outputs and display with rich

- [ ] 11.0 Generate final report with rich output
  - [ ] 11.1 Assemble report sections and metadata
  - [ ] 11.2 Verify formatting against renderer tests
  - [ ] 11.3 Provide downloadable artifact (e.g., markdown export)

- [ ] 12.0 Integrate structured logging and LangSmith tracing (after final report & toggles)
  - [ ] 12.1 Enable structured logs around key steps
  - [ ] 12.2 Add optional LangSmith tracing hooks (guarded by env var)
  - [ ] 12.3 Show minimal trace visualization or link to UI

- [ ] 13.0 Compare prompts and LLM settings side-by-side
  - [ ] 13.1 Vary prompts; compare outputs deterministically
  - [ ] 13.2 Demonstrate temperature/max_tokens effects
  - [ ] 13.3 Summarize best practices and trade-offs

- [ ] 14.0 Initialize MCP server, discover and list tools (lower priority)
  - [ ] 14.1 Start simple in-process MCP stub
  - [ ] 14.2 Discover tools and enumerate capabilities
  - [ ] 14.3 Explain async usage patterns

- [ ] 15.0 Demonstrate MCP filesystem operations and error handling
  - [ ] 15.1 Read local docs via MCP file tool
  - [ ] 15.2 Handle expected errors and show safe patterns
  - [ ] 15.3 Provide mock fallback for deterministic runs

- [ ] 16.0 Benchmark mock vs live and LLM settings
  - [ ] 16.1 Measure latency for representative steps
  - [ ] 16.2 Compare throughput/variability under different settings
  - [ ] 16.3 Present results in a concise table

- [ ] 17.0 Write troubleshooting, pitfalls, and best practices
  - [ ] 17.1 Common setup issues and resolutions
  - [ ] 17.2 Prompt/LLM pitfalls and mitigations
  - [ ] 17.3 Links to deeper references

- [ ] 18.0 Include TDD mini-example mirroring existing tests
  - [ ] 18.1 Write assertions first, then add minimal code to pass
  - [ ] 18.2 Show test-driven loop in notebook
  - [ ] 18.3 Map to actual pytest in repo

- [ ] 19.0 Final review against PRD success metrics
  - [ ] 19.1 Verify educational coverage and clarity
  - [ ] 19.2 Confirm deterministic runs and live labels
  - [ ] 19.3 Ensure notebook-to-test mapping completeness

### Continuous Across All Tasks

- [ ] C.1 Map notebook sections to corresponding test cases
- [ ] C.2 Ensure docstrings, comments, and type hints throughout
- [ ] C.3 Run pytest continuously; keep examples aligned with tests
- [ ] C.4 Add assertpy validations alongside outputs
