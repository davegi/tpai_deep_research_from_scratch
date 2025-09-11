import os

from research_agent_framework.helpers.switchboard import use_mock_search, use_mock_llm
from research_agent_framework.config import get_settings


def test_use_mock_search_when_no_keys(monkeypatch):
    monkeypatch.delenv("SERPAPI_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    assert use_mock_search() is True


def test_use_mock_search_force(monkeypatch):
    monkeypatch.setenv("FORCE_USE_MOCK", "1")
    assert use_mock_search() is True
    monkeypatch.delenv("FORCE_USE_MOCK", raising=False)


def test_use_mock_llm_defaults(monkeypatch):
    # ensure settings model_name is default (mock-model)
    s = get_settings(force_reload=True)
    assert use_mock_llm(s) is True


def test_use_mock_llm_respects_model_name(monkeypatch):
    # simulate a real model name via env shim
    monkeypatch.setenv("MODEL_NAME", "openai")
    s = get_settings(force_reload=True)
    assert use_mock_llm(s) is False
    monkeypatch.delenv("MODEL_NAME", raising=False)
