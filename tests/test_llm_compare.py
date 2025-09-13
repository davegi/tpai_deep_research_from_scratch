import pytest
import asyncio
from assertpy import assert_that
from research_agent_framework.llm.client import LLMConfig
from research_agent_framework.llm.compare import compare_prompts, compare_settings, compare_all

@pytest.mark.asyncio
async def test_compare_prompts_basic():
    prompts = ["Hello!", "What is AI?", "Summarize coffee shops in SF."]
    config = LLMConfig(api_key="test", model="mock-model")
    results = await compare_prompts(prompts, config)
    for prompt in prompts:
        assert_that(results).contains_key(prompt)
        assert_that(results[prompt]).contains("mock response for:")

@pytest.mark.asyncio
async def test_compare_settings_basic():
    prompt = "Test prompt for settings."
    configs = [
        LLMConfig(api_key="test", model="mock-model", temperature=0.0, max_tokens=32),
        LLMConfig(api_key="test", model="mock-model", temperature=1.0, max_tokens=128),
    ]
    results = await compare_settings(prompt, configs)
    for label, output in results.items():
        assert_that(label).contains("model=mock-model")
        assert_that(output).contains("mock response for:")

@pytest.mark.asyncio
async def test_compare_all_basic():
    prompts = ["Prompt 1", "Prompt 2"]
    configs = [
        LLMConfig(api_key="test", model="mock-model", temperature=0.5, max_tokens=64),
        LLMConfig(api_key="test", model="mock-model", temperature=1.5, max_tokens=256),
    ]
    results = await compare_all(prompts, configs)
    for prompt in prompts:
        assert_that(results).contains_key(prompt)
        for label, output in results[prompt].items():
            assert_that(label).contains("model=mock-model")
            assert_that(output).contains("mock response for:")
