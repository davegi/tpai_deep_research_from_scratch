import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parents[1]
src = repo_root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

# quick import smoke test
from research_agent_framework.llm.client import MockLLM, LLMConfig
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
try:
    from research_agent_framework.config import get_logger
    logger = get_logger()
    logger.info('imports ok: %s %s', MockLLM is not None, MockSearchAdapter is not None)
except Exception:
    # Fallback to Console for human-readable output
    try:
        from rich.console import Console
        Console().print('imports ok:', MockLLM is not None, MockSearchAdapter is not None)
    except Exception:
        # Last resort
        print('imports ok:', MockLLM is not None, MockSearchAdapter is not None)
