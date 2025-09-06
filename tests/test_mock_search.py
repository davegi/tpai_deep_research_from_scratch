import pytest
import asyncio
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
from research_agent_framework.models import SerpResult


@pytest.mark.asyncio
async def test_mock_search_returns_serpresults():
    adapter = MockSearchAdapter()
    results = await adapter.search("best coffee")
    assert isinstance(results, list)
    assert len(results) == 2
    for r in results:
        assert isinstance(r, SerpResult)
        assert r.title
        assert r.url
        assert isinstance(r.raw, dict)
