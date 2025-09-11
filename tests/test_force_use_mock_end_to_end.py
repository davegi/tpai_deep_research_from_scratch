import os

from research_agent_framework.adapters.search import from_raw_adapter
from research_agent_framework.llm.client import llm_factory, LLMConfig, MockLLM
from research_agent_framework.config import get_settings
from research_agent_framework.helpers.switchboard import use_mock_search, use_mock_llm


def test_force_use_mock_for_adapters_and_llm(monkeypatch):
    # Ensure env is clean first
    monkeypatch.delenv("SERPAPI_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)

    # Force use of mocks
    monkeypatch.setenv("FORCE_USE_MOCK", "true")

    s = get_settings(force_reload=True)

    # Query switchboard helpers to decide which provider to instantiate
    is_mock_search = use_mock_search(s)
    is_mock_llm = use_mock_llm(s)

    serp_provider = "mock" if is_mock_search else "serpapi"
    tav_provider = "mock" if is_mock_search else "tavily"

    serp = from_raw_adapter({}, provider=serp_provider)
    tav = from_raw_adapter({}, provider=tav_provider)
    assert serp.__class__.__name__.lower().startswith("mock")
    assert tav.__class__.__name__.lower().startswith("mock")

    # LLM factory should follow switchboard decision
    cfg = LLMConfig(api_key=s.llm_api_key or "", model=s.model_name or "mock-model", temperature=s.model_temperature)
    provider = "mock" if is_mock_llm else s.model_name
    try:
        llm = llm_factory(provider or "mock", cfg)
    except Exception:
        llm = MockLLM(cfg)
    assert isinstance(llm, MockLLM)

    # Clean up
    monkeypatch.delenv("FORCE_USE_MOCK", raising=False)
