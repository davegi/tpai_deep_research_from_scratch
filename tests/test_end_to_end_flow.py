import pytest
import asyncio

from research_agent_framework.llm.client import MockLLM, LLMConfig, llm_factory
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
from assertpy import assert_that


@pytest.mark.asyncio
async def test_minimal_end_to_end_flow():
    # Mock LLM
    config = LLMConfig(api_key="test", model="mock-model")
    llm = MockLLM(config)

    # Mock search
    search = MockSearchAdapter()

    # Simulate a simple agent workflow: search -> LLM summarization
    serp_results = await search.search("best coffee in SF")
    # Normalize results to a concrete list and prepare titles safely
    serp_results_list = getattr(serp_results, 'results', serp_results)
    if not isinstance(serp_results_list, list):
        serp_results_list = list(serp_results_list)
    titles = ", ".join(getattr(r, 'title', r[0] if isinstance(r, tuple) and len(r) > 0 else '') for r in serp_results_list)
    prompt = f"Summarize these coffee shops: {titles}"
    summary = await llm.generate(prompt)

    assert_that(summary, description="LLM.generate should return a string").is_instance_of(str)
    assert_that(summary, description="MockLLM output should include mock response marker").contains("mock response for:")
