import pytest

from research_agent_framework.adapters.search.serpapi_search import SerpAPISearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest


def test_serpapi_from_raw_exists():
    adapter = SerpAPISearchAdapter.from_raw({"provider": "serpapi-stub"})
    assert isinstance(adapter, SerpAPISearchAdapter)


@pytest.mark.asyncio
async def test_serpapi_search_returns_serp_reply_and_preserves_raw():
    adapter = SerpAPISearchAdapter()
    req = SerpRequest(query="test query", limit=1)
    reply = await adapter.search(req)
    assert hasattr(reply, 'results')
    assert reply.meta.provider == 'serpapi-stub'
    assert isinstance(reply.results, list)
    assert len(reply.results) == 1
    r = reply.results[0]
    assert isinstance(r.raw, dict)
    assert r.raw.get('query') == 'test query'


@pytest.mark.asyncio
async def test_serpapi_empty_limit_returns_empty():
    adapter = SerpAPISearchAdapter()
    req = SerpRequest(query='x', limit=0)
    reply = await adapter.search(req)
    assert isinstance(reply.results, list)
    assert len(reply.results) == 0
