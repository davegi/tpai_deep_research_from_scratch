import pytest

from research_agent_framework.adapters.search.tavily_search import TavilySearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply, ReplyMeta


def test_tavily_from_raw_exists():
    adapter = TavilySearchAdapter.from_raw({"provider": "tavily-stub"})
    assert isinstance(adapter, TavilySearchAdapter)


@pytest.mark.asyncio
async def test_tavily_search_returns_serp_reply_and_preserves_raw():
    adapter = TavilySearchAdapter()
    req = SerpRequest(query="espresso", limit=1)
    reply = await adapter.search(req)
    assert isinstance(reply, SerpReply)
    assert reply.meta.provider == 'tavily-stub'
    assert len(reply.results) == 1
    r = reply.results[0]
    assert isinstance(r.raw, dict)
    assert r.raw.get('query') == 'espresso'


@pytest.mark.asyncio
async def test_tavily_empty_limit_returns_empty():
    adapter = TavilySearchAdapter()
    req = SerpRequest(query='x', limit=0)
    reply = await adapter.search(req)
    assert isinstance(reply.results, list)
    assert len(reply.results) == 0


def test_tavily_from_raw_malformed_url_preserved():
    # The stub's from_raw should accept arbitrary raw payloads; ensure
    # caller-provided malformed url is preserved by construction of
    # adapter (actual SerpResult construction happens in search but we
    # ensure factory does not attempt validation here).
    raw: dict[str, object] = {"provider": "tavily-stub", "url": "not-a-url"}
    adapter = TavilySearchAdapter.from_raw(raw)
    assert isinstance(adapter, TavilySearchAdapter)
