import sys
from pathlib import Path
# Ensure repository `src` package is importable when running this script directly
repo_root = Path(__file__).resolve().parents[1]
src = repo_root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

import asyncio
from research_agent_framework.llm.client import MockLLM, LLMConfig
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter

async def run():
    cfg = LLMConfig(api_key='x', model='m')
    llm = MockLLM(cfg)
    sr = MockSearchAdapter()
    out = await llm.generate('hello')
    results = await sr.search('hello')
    print('LLM:', out)
    print('Results count:', len(results))
    for r in results:
        print('-', r.title)

if __name__ == '__main__':
    asyncio.run(run())
