import os
import pytest

from research_agent_framework.adapters.search.tavily_search import TavilySearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest
from assertpy import assert_that


@pytest.mark.skipif(
    not os.getenv("TAVILY_API_KEY"), reason="TAVILY_API_KEY not set; skipping network test"
)
def test_tavily_network_search_runs():
    adapter = TavilySearchAdapter(api_key=os.getenv("TAVILY_API_KEY"))
    import asyncio

    async def run():
        reply = await adapter.search(SerpRequest(query="museum near me", limit=1))
        assert_that(reply.meta.provider).is_not_none()

    asyncio.run(run())
