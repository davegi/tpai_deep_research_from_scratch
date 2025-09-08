import pytest

from pydantic import ValidationError

from research_agent_framework.adapters.search.schema import SerpRequest
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
from assertpy import assert_that


def test_serp_request_validation():
    with pytest.raises(ValidationError):
        SerpRequest(query="")


@pytest.mark.asyncio
async def test_mock_search_adapter_return_serp_reply():
    adapter = MockSearchAdapter()
    # Use SerpRequest
    req = SerpRequest(query="best coffee", limit=2)
    reply = await adapter.search(req)
    # Support both SerpReply and legacy list return
    from research_agent_framework.adapters.search.schema import SerpReply
    if isinstance(reply, SerpReply):
        assert_that(getattr(reply.meta, 'provider', None), description="SerpReply.meta.provider should be 'mock'").is_equal_to("mock")
        results_list = list(reply.results)
    else:
        results_list = list(reply)

    assert_that(len(results_list), description="SerpReply should contain two results").is_equal_to(2)
    for r in results_list:
        if isinstance(r, tuple):
            # legacy tuple shape: (title, url, snippet, raw)
            raw = r[3] if len(r) > 3 else {}
            source = raw.get('source') if isinstance(raw, dict) else None
            assert_that(source, description="each result raw.source should be 'mock'").is_equal_to('mock')
        else:
            assert_that(getattr(r, 'raw', None) and r.raw.get('source'), description="each result raw.source should be 'mock'").is_equal_to('mock')


@pytest.mark.asyncio
async def test_mock_search_adapter_backwards_compatibility():
    adapter = MockSearchAdapter()
    # Back-compat: when called with a plain string the adapter returns a list of SerpResult objects (legacy behavior). New callers should
    # use `SerpRequest` -> `SerpReply`.
    reply = await adapter.search("best coffee")
    # Back-compat: should return a list of SerpResult
    results_list = getattr(reply, 'results', reply)
    # Normalize to list for static typing
    if not isinstance(results_list, list):
        results_list = list(results_list)
    assert_that(results_list, description="Back-compat call should return a list").is_instance_of(list)
    assert_that(len(results_list), description="Back-compat list should have two items").is_equal_to(2)
    # Inspect items
    for r in results_list:
        if isinstance(r, tuple):
            raw = r[3] if len(r) > 3 else {}
            source = raw.get('source') if isinstance(raw, dict) else None
            assert_that(source, description="legacy result raw.source should be 'mock'").is_equal_to('mock')
        else:
            assert_that(getattr(r, 'raw', None) and r.raw.get('source'), description="legacy result raw.source should be 'mock'").is_equal_to('mock')
