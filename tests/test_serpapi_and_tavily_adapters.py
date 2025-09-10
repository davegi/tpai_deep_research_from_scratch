import pytest

from research_agent_framework.adapters.search.serpapi_search import SerpAPISearchAdapter
from research_agent_framework.adapters.search.tavily_search import TavilySearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply
from assertpy import assert_that


@pytest.mark.asyncio
async def test_serpapi_adapter_from_raw_and_search():
    adapter = SerpAPISearchAdapter.from_raw({'provider': 'serpapi-stub'})
    reply = await adapter.search(SerpRequest(query='x', limit=1))
    assert_that(reply).is_instance_of(SerpReply)
    assert_that(len(list(reply.results))).is_equal_to(1)
    assert_that((reply.meta.provider == 'serpapi-stub') or (reply.meta.provider == 'serpapi')).is_true()


@pytest.mark.asyncio
async def test_serpapi_adapter_limit_zero():
    adapter = SerpAPISearchAdapter.from_raw({'provider': 'serpapi-stub'})
    reply = await adapter.search(SerpRequest(query='x', limit=0))
    assert_that(reply).is_instance_of(SerpReply)
    assert_that(len(list(reply.results))).is_equal_to(0)


@pytest.mark.asyncio
async def test_tavily_adapter_from_raw_and_search():
    adapter = TavilySearchAdapter.from_raw({'provider': 'tavily-stub'})
    reply = await adapter.search(SerpRequest(query='x', limit=1))
    assert_that(reply).is_instance_of(SerpReply)
    assert_that(len(list(reply.results))).is_equal_to(1)
    assert_that((reply.meta.provider == 'tavily-stub') or (reply.meta.provider == 'tavily')).is_true()


@pytest.mark.asyncio
async def test_tavily_adapter_limit_zero():
    adapter = TavilySearchAdapter.from_raw({'provider': 'tavily-stub'})
    reply = await adapter.search(SerpRequest(query='x', limit=0))
    assert_that(reply).is_instance_of(SerpReply)
    assert_that(len(list(reply.results))).is_equal_to(0)
