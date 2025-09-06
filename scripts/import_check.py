import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parents[1]
src = repo_root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

# quick import smoke test
from research_agent_framework.llm.client import MockLLM, LLMConfig
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
print('imports ok:', MockLLM is not None, MockSearchAdapter is not None)
