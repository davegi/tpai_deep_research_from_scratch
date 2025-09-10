import os
import pytest

from research_agent_framework.adapters.search.tavily_search import TavilySearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest


@pytest.mark.skipif(
    not os.getenv("TAVILY_API_KEY"), reason="TAVILY_API_KEY not set; skipping network test"
)
def test_tavily_network_search_runs():
    adapter = TavilySearchAdapter(api_key=os.getenv("TAVILY_API_KEY"))
    import asyncio

    async def run():
        reply = await adapter.search(SerpRequest(query="museum near me", limit=1))
        assert reply.meta.provider is not None

    asyncio.run(run())
