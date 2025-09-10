import os
import pytest

from research_agent_framework.adapters.search.serpapi_search import SerpAPISearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest


@pytest.mark.skipif(
    not os.getenv("SERPAPI_API_KEY"), reason="SERPAPI_API_KEY not set; skipping network test"
)
def test_serpapi_network_search_runs():
    adapter = SerpAPISearchAdapter(api_key=os.getenv("SERPAPI_API_KEY"))
    # Use a short sync wrapper to call the async search
    import asyncio

    async def run():
        reply = await adapter.search(SerpRequest(query="coffee near me", limit=1))
        assert reply.meta.provider is not None

    asyncio.run(run())
