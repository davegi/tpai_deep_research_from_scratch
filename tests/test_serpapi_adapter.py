import pytest

from research_agent_framework.adapters.search.serpapi_search import SerpAPISearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest
from assertpy import assert_that


def test_serpapi_from_raw_exists():
    adapter = SerpAPISearchAdapter.from_raw({"provider": "serpapi-stub"})
    assert_that(adapter).is_instance_of(SerpAPISearchAdapter)


@pytest.mark.asyncio
async def test_serpapi_search_returns_serp_reply_and_preserves_raw():
    adapter = SerpAPISearchAdapter()
    req = SerpRequest(query="test query", limit=1)
    reply = await adapter.search(req)
    assert_that(hasattr(reply, 'results')).is_true()
    assert_that(reply.meta.provider).is_equal_to('serpapi-stub')
    assert_that(reply.results).is_instance_of(list)
    assert_that(len(reply.results)).is_equal_to(1)
    r = reply.results[0]
    assert_that(isinstance(r.raw, dict)).is_true()
    assert_that(r.raw.get('query')).is_equal_to('test query')


@pytest.mark.asyncio
async def test_serpapi_empty_limit_returns_empty():
    adapter = SerpAPISearchAdapter()
    req = SerpRequest(query='x', limit=0)
    reply = await adapter.search(req)
    assert_that(reply.results).is_instance_of(list)
    assert_that(len(reply.results)).is_equal_to(0)
