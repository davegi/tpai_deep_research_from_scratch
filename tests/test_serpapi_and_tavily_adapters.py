import pytest

from research_agent_framework.adapters.search.serpapi_search import SerpAPISearchAdapter
from research_agent_framework.adapters.search.tavily_search import TavilySearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply


@pytest.mark.asyncio
async def test_serpapi_adapter_from_raw_and_search():
    adapter = SerpAPISearchAdapter.from_raw({'provider': 'serpapi-stub'})
    reply = await adapter.search(SerpRequest(query='x', limit=1))
    assert isinstance(reply, SerpReply)
    assert len(list(reply.results)) == 1
    assert reply.meta.provider == 'serpapi-stub' or reply.meta.provider == 'serpapi'


@pytest.mark.asyncio
async def test_serpapi_adapter_limit_zero():
    adapter = SerpAPISearchAdapter.from_raw({'provider': 'serpapi-stub'})
    reply = await adapter.search(SerpRequest(query='x', limit=0))
    assert isinstance(reply, SerpReply)
    assert len(list(reply.results)) == 0


@pytest.mark.asyncio
async def test_tavily_adapter_from_raw_and_search():
    adapter = TavilySearchAdapter.from_raw({'provider': 'tavily-stub'})
    reply = await adapter.search(SerpRequest(query='x', limit=1))
    assert isinstance(reply, SerpReply)
    assert len(list(reply.results)) == 1
    assert reply.meta.provider == 'tavily-stub' or reply.meta.provider == 'tavily'


@pytest.mark.asyncio
async def test_tavily_adapter_limit_zero():
    adapter = TavilySearchAdapter.from_raw({'provider': 'tavily-stub'})
    reply = await adapter.search(SerpRequest(query='x', limit=0))
    assert isinstance(reply, SerpReply)
    assert len(list(reply.results)) == 0
