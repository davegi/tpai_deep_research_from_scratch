import sys
from pathlib import Path
from typing import List

from research_agent_framework.adapters.search.schema import SerpReply
from research_agent_framework.models import SerpResult
# Ensure repository `src` package is importable when running this script directly
repo_root = Path(__file__).resolve().parents[1]
src = repo_root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

import asyncio
from research_agent_framework.llm.client import MockLLM, LLMConfig
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
from research_agent_framework.config import get_logger

async def run():
    cfg = LLMConfig(api_key='x', model='m')
    llm = MockLLM(cfg)
    sr = MockSearchAdapter()
    out = await llm.generate('hello')
    results: List[SerpResult] | SerpReply = await sr.search('hello')
    logger = get_logger()
    logger.info('LLM: %s', out)
    # len() may not be available on SerpReply; guard for attribute
    results_list = getattr(results, 'results', results)
    if not isinstance(results_list, list):
        try:
            results_list = list(results_list)
        except TypeError:
            results_list = [results_list]
    count = len(results_list)
    logger.info('Results count: %s', count)
    for r in getattr(results, 'results', results):
        title = getattr(r, 'title', None)
        logger.info('-', title)

if __name__ == '__main__':
    asyncio.run(run())
