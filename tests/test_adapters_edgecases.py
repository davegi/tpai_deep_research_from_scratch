import pytest
from typing import cast

from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply
from research_agent_framework.models import SerpResult


@pytest.mark.asyncio
async def test_mock_search_empty_query_backcompat_and_serpreply():
    adapter = MockSearchAdapter()
    # Back-compat string call
    res = await adapter.search("")
    if isinstance(res, list):
        assert res == []
    else:
        # New contract: SerpReply with empty results
        assert isinstance(res, SerpReply)
        assert list(res.results) == []


@pytest.mark.asyncio
async def test_mock_search_serprequest_limit_zero_returns_empty_reply():
    adapter = MockSearchAdapter()
    req = SerpRequest(query="some query", limit=0)
    reply = await adapter.search(req)
    assert isinstance(reply, SerpReply)
    assert list(reply.results) == []
    assert getattr(reply.meta, 'total_results', 0) == 0


def test_serpresult_from_raw_rejects_non_dict():
    # Use cast to intentionally pass a non-dict at runtime while satisfying static type checkers
    bad_raw = cast(dict, "not-a-dict")
    with pytest.raises(TypeError):
        SerpResult.from_raw(bad_raw)
