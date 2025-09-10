import pytest

from research_agent_framework.adapters.search.tavily_search import TavilySearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply, ReplyMeta
from assertpy import assert_that


def test_tavily_from_raw_exists():
    adapter = TavilySearchAdapter.from_raw({"provider": "tavily-stub"})
    assert_that(adapter).is_instance_of(TavilySearchAdapter)


@pytest.mark.asyncio
async def test_tavily_search_returns_serp_reply_and_preserves_raw():
    adapter = TavilySearchAdapter()
    req = SerpRequest(query="espresso", limit=1)
    reply = await adapter.search(req)
    assert_that(reply).is_instance_of(SerpReply)
    assert_that(reply.meta.provider).is_equal_to('tavily-stub')
    assert_that(len(reply.results)).is_equal_to(1)
    r = reply.results[0]
    assert_that(isinstance(r.raw, dict)).is_true()
    assert_that(r.raw.get('query')).is_equal_to('espresso')


@pytest.mark.asyncio
async def test_tavily_empty_limit_returns_empty():
    adapter = TavilySearchAdapter()
    req = SerpRequest(query='x', limit=0)
    reply = await adapter.search(req)
    assert_that(reply.results).is_instance_of(list)
    assert_that(len(reply.results)).is_equal_to(0)


def test_tavily_from_raw_malformed_url_preserved():
    # The stub's from_raw should accept arbitrary raw payloads; ensure
    # caller-provided malformed url is preserved by construction of
    # adapter (actual SerpResult construction happens in search but we
    # ensure factory does not attempt validation here).
    raw: dict[str, object] = {"provider": "tavily-stub", "url": "not-a-url"}
    adapter = TavilySearchAdapter.from_raw(raw)
    assert_that(adapter).is_instance_of(TavilySearchAdapter)
