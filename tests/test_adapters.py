import pytest

from pydantic import ValidationError

from research_agent_framework.adapters.search.schema import SerpRequest
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter


def test_serprequest_validation():
    with pytest.raises(ValidationError):
        SerpRequest(query="")


@pytest.mark.asyncio
async def test_mocksearchadapter_returns_serpreply_and_preserves_raw():
    adapter = MockSearchAdapter()
    # Use SerpRequest
    req = SerpRequest(query="best coffee", limit=2)
    reply = await adapter.search(req)
    assert reply.meta.provider == "mock"
    assert len(reply.results) == 2
    for r in reply.results:
        assert r.raw.get('source') == 'mock'


@pytest.mark.asyncio
async def test_mocksearchadapter_backcompat_with_str():
    adapter = MockSearchAdapter()
    # Back-compat: when called with a plain string the adapter returns a list
    # of SerpResult objects (legacy behavior). New callers should use
    # `SerpRequest` -> `SerpReply`.
    reply = await adapter.search("best coffee")
    assert isinstance(reply, list)
    assert len(reply) == 2
    # Inspect items
    for r in reply:
        assert r.raw.get('source') == 'mock'
