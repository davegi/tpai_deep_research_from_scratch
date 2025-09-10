import pytest
from typing import cast

from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply
from research_agent_framework.models import SerpResult
from typing import cast
from assertpy import assert_that


@pytest.mark.asyncio
async def test_mock_search_empty_query_backcompat_and_serpreply():
    adapter = MockSearchAdapter()
    # Back-compat string call
    res = await adapter.search("")
    if isinstance(res, list):
        assert_that(res).is_equal_to([])
    else:
        # New contract: SerpReply with empty results
        assert_that(res).is_instance_of(SerpReply)
        reply = cast(SerpReply, res)
        assert_that(list(reply.results)).is_equal_to([])


@pytest.mark.asyncio
async def test_mock_search_serprequest_limit_zero_returns_empty_reply():
    adapter = MockSearchAdapter()
    req = SerpRequest(query="some query", limit=0)
    reply = await adapter.search(req)
    assert_that(reply).is_instance_of(SerpReply)
    reply = cast(SerpReply, reply)
    assert_that(list(reply.results)).is_equal_to([])
    assert_that(getattr(reply.meta, 'total_results', 0)).is_equal_to(0)


def test_serpresult_from_raw_rejects_non_dict():
    # Use cast to intentionally pass a non-dict at runtime while satisfying static type checkers
    bad_raw = cast(dict, "not-a-dict")
    with pytest.raises(TypeError):
        SerpResult.from_raw(bad_raw)
