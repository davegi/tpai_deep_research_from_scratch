
import pytest
import asyncio
from assertpy import assert_that
from src.research_agent_framework.llm.client import (
    LLMConfig, OpenAIConfig, AnthropicConfig, MockLLM, llm_factory
)

@pytest.mark.asyncio
async def test_mockllm_generate():
    config = LLMConfig(api_key="test", model="mock-model")
    client = MockLLM(config)
    result = await client.generate("Hello!")
    assert_that(result, "MockLLM should return deterministic output for given prompt.").is_equal_to("mock response for: Hello!")

@pytest.mark.asyncio
async def test_factory_openai():
    config = LLMConfig(api_key="sk-xxx", model="gpt-4")
    client = llm_factory("openai", config)
    assert_that(hasattr(client, "generate"), "OpenAIClient should have a 'generate' method.").is_true()
    result = await client.generate("Test")
    assert_that(result, "OpenAIClient should return expected mock response.").is_equal_to("openai response")

@pytest.mark.asyncio
async def test_factory_anthropic():
    config = LLMConfig(api_key="sk-yyy", model="claude-3")
    client = llm_factory("anthropic", config)
    assert_that(hasattr(client, "generate"), "AnthropicClient should have a 'generate' method.").is_true()
    result = await client.generate("Test")
    assert_that(result, "AnthropicClient should return expected mock response.").is_equal_to("anthropic response")

@pytest.mark.asyncio
async def test_factory_stubbed():
    config = LLMConfig(api_key="stub", model="stub-model")
    for provider in ["gemini", "cohere", "mistral", "copilot", "huggingface", "azure-openai"]:
        client = llm_factory(provider, config)
        with pytest.raises(NotImplementedError):
            await client.generate("Test")

@pytest.mark.asyncio
async def test_factory_invalid_provider():
    config = LLMConfig(api_key="stub", model="stub-model")
    with pytest.raises(ValueError):
        llm_factory("unknown", config)
