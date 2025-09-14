from research_agent_framework.llm.client import llm_factory, LLMConfig, MockLLM, OpenAIClient


def test_llm_factory_returns_mock_for_mock_provider():
    cfg = LLMConfig(api_key="", model="mock", temperature=0.0)
    client = llm_factory("mock", cfg)
    from assertpy import assert_that
    assert_that(client, description="llm_factory should return MockLLM for 'mock' provider").is_instance_of(MockLLM)


def test_llm_factory_returns_openai_for_openai_provider():
    cfg = LLMConfig(api_key="fake", model="openai", temperature=0.0)
    client = llm_factory("openai", cfg)
    from assertpy import assert_that
    assert_that(client.__class__.__name__, description="llm_factory should return OpenAIClient for 'openai' provider").is_equal_to("OpenAIClient")
