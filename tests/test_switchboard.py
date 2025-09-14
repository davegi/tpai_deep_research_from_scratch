import os

from research_agent_framework.helpers.switchboard import use_mock_search, use_mock_llm
from research_agent_framework.config import get_settings


def test_use_mock_search_when_no_keys(monkeypatch):
    monkeypatch.delenv("SERPAPI_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    from assertpy import assert_that
    assert_that(use_mock_search(), description="use_mock_search should be True when no API keys are set").is_true()


def test_use_mock_search_force(monkeypatch):
    monkeypatch.setenv("FORCE_USE_MOCK", "1")
    from assertpy import assert_that
    assert_that(use_mock_search(), description="use_mock_search should be True when FORCE_USE_MOCK is set").is_true()
    monkeypatch.delenv("FORCE_USE_MOCK", raising=False)


def test_use_mock_llm_defaults(monkeypatch):
    # ensure settings model_name is default (mock-model)
    s = get_settings(force_reload=True)
    from assertpy import assert_that
    assert_that(use_mock_llm(s), description="use_mock_llm should be True for default mock-model").is_true()


def test_use_mock_llm_respects_model_name(monkeypatch):
    # simulate a real model name via env shim
    monkeypatch.setenv("MODEL_NAME", "openai")
    s = get_settings(force_reload=True)
    from assertpy import assert_that
    assert_that(use_mock_llm(s), description="use_mock_llm should be False for real model name").is_false()
    monkeypatch.delenv("MODEL_NAME", raising=False)
