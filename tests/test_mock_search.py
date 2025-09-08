import pytest
import asyncio
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
from research_agent_framework.models import SerpResult
from assertpy import assert_that


@pytest.mark.asyncio
async def test_mock_search_yields_serp_results():
    adapter = MockSearchAdapter()
    results = await adapter.search("best coffee")
    # Normalize to a concrete list for static typing
    results_raw = getattr(results, "results", None)
    if results_raw is not None:
        results_list: list = list(results_raw)
    else:
        if isinstance(results, list):
            results_list = results
        else:
            try:
                results_list = list(results)
            except TypeError:
                results_list = [results]

    assert_that(results_list, description="MockSearchAdapter.search should return a list in back-compat mode").is_instance_of(list)
    assert_that(len(results_list), description="MockSearchAdapter should return two canned results").is_equal_to(2)
    for r in results_list:
        assert_that(r, description="Individual result should be a SerpResult").is_instance_of(SerpResult)
        assert_that(getattr(r, 'title', None), description="result.title should be present").is_not_empty()
        assert_that(getattr(r, 'url', None), description="result.url should be present").is_not_none()
        # Support legacy tuple shapes defensively
        if isinstance(r, tuple):
            assert_that(len(r)).is_greater_than(0)
        else:
            assert_that(isinstance(r.raw, dict), description="result.raw should be a dict").is_true()
