import importlib
import importlib.util
import pytest

# Attempt to import respx at runtime; if unavailable, tests will be skipped.
_respx_spec = importlib.util.find_spec("respx")
if _respx_spec is None:
    pytest.skip("respx not installed; skipping network-mocked tests", allow_module_level=True)

import respx as _respx
import httpx

from research_agent_framework.adapters.search.serpapi_search import SerpAPISearchAdapter
from research_agent_framework.adapters.search.tavily_search import TavilySearchAdapter
from research_agent_framework.adapters.search.schema import SerpRequest


def test_serpapi_adapter_handles_mocked_response():
    endpoint = "https://serpapi.test/search"
    adapter = SerpAPISearchAdapter(api_key="fake", endpoint=endpoint)

    mocked = _respx.mock
    with mocked:
        mocked.get(endpoint).respond(200, json={"results": [{"title": "Mocked title", "link": "https://x/1"}]})

        import asyncio

        async def run():
            from assertpy import assert_that
            reply = await adapter.search(SerpRequest(query="q", limit=1))
            assert_that(reply.meta.total_results).is_equal_to(1)
            assert_that(reply.results[0].title).is_equal_to("Mocked title")

        asyncio.run(run())


def test_tavily_adapter_handles_mocked_response():
    endpoint = "https://tavily.test/search"
    adapter = TavilySearchAdapter(api_key="fake", endpoint=endpoint)

    mocked = _respx.mock
    with mocked:
        mocked.get(endpoint).respond(200, json={"results": [{"name": "Tavily item", "href": "https://x/2"}]})

        import asyncio

        async def run():
            from assertpy import assert_that
            reply = await adapter.search(SerpRequest(query="q", limit=1))
            assert_that(reply.meta.total_results).is_equal_to(1)
            assert_that(reply.results[0].title).is_equal_to("Tavily item")

        asyncio.run(run())
