import pytest
import asyncio

from research_agent_framework.llm.client import MockLLM, LLMConfig, llm_factory
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter


@pytest.mark.asyncio
async def test_minimal_end_to_end_flow():
    # Mock LLM
    config = LLMConfig(api_key="test", model="mock-model")
    llm = MockLLM(config)

    # Mock search
    search = MockSearchAdapter()

    # Simulate a simple agent workflow: search -> LLM summarization
    serp_results = await search.search("best coffee in SF")
    # Prepare a prompt summarizing titles
    titles = ", ".join(r.title for r in serp_results)
    prompt = f"Summarize these coffee shops: {titles}"
    summary = await llm.generate(prompt)

    assert isinstance(summary, str)
    assert "mock response for:" in summary
