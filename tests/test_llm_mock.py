

import pytest
import asyncio
from assertpy import assert_that
from research_agent_framework.llm.client import LLMConfig, MockLLM, llm_factory
from hypothesis import given, strategies as st

class TestLLMClient:
    @pytest.mark.asyncio
    async def test_mockllm_generate(self):
        config = LLMConfig(api_key="test", model="mock-model")
        client = MockLLM(config)
        result = await client.generate("Hello!")
        assert_that(result, "MockLLM should return deterministic output for given prompt.").is_equal_to("mock response for: Hello!")

    @pytest.mark.asyncio
    async def test_factory_openai(self):
        config = LLMConfig(api_key="sk-xxx", model="gpt-4")
        client = llm_factory("openai", config)
        assert_that(hasattr(client, "generate"), "OpenAIClient should have a 'generate' method.").is_true()
        result = await client.generate("Test")
        assert_that(result, "OpenAIClient should return expected mock response.").is_equal_to("openai response")

    @pytest.mark.asyncio
    async def test_factory_anthropic(self):
        config = LLMConfig(api_key="sk-yyy", model="claude-3")
        client = llm_factory("anthropic", config)
        assert_that(hasattr(client, "generate"), "AnthropicClient should have a 'generate' method.").is_true()
        result = await client.generate("Test")
        assert_that(result, "AnthropicClient should return expected mock response.").is_equal_to("anthropic response")

    @pytest.mark.asyncio
    async def test_factory_stubbed(self):
        config = LLMConfig(api_key="stub", model="stub-model")
        for provider in ["gemini", "cohere", "mistral", "copilot", "huggingface", "azure-openai"]:
            client = llm_factory(provider, config)
            with pytest.raises(NotImplementedError):
                await client.generate("Test")

    @pytest.mark.asyncio
    async def test_factory_invalid_provider(self):
        config = LLMConfig(api_key="stub", model="stub-model")
        with pytest.raises(ValueError):
            llm_factory("unknown", config)

    # Property-based tests
    @pytest.mark.hypothesis
    @pytest.mark.asyncio
    @given(
        prompt=st.text(min_size=1, max_size=200),
        api_key=st.text(min_size=1, max_size=20),
        model=st.text(min_size=1, max_size=20)
    )
    async def test_mockllm_property_valid(self, prompt, api_key, model):
        config = LLMConfig(api_key=api_key, model=model)
        client = MockLLM(config)
        result = await client.generate(prompt)
        assert_that(result).is_equal_to(f"mock response for: {prompt}")

    @pytest.mark.hypothesis
    @pytest.mark.asyncio
    @given(
        provider=st.sampled_from(["gemini", "cohere", "mistral", "copilot", "huggingface", "azure-openai"]),
        api_key=st.text(min_size=1, max_size=20),
        model=st.text(min_size=1, max_size=20),
        prompt=st.text(min_size=1, max_size=200)
    )
    async def test_factory_stubbed_property(self, provider, api_key, model, prompt):
        config = LLMConfig(api_key=api_key, model=model)
        client = llm_factory(provider, config)
        with pytest.raises(NotImplementedError):
            await client.generate(prompt)
