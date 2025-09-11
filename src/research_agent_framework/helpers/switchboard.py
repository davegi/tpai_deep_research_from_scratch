"""Helper utilities to determine whether to use mock or live providers.

This centralizes the small environment-driven logic used by the notebook demos
so the behaviour can be unit-tested.
"""
import os
from typing import Optional

from research_agent_framework.config import get_settings


def use_mock_search(settings=None) -> bool:
    """Return True when search adapters should default to mock.

    Priority:
    1. If explicit env var `FORCE_USE_MOCK` is set to a truthy value -> True
    2. If provider keys (SERPAPI_API_KEY/TAVILY_API_KEY) are missing -> True
    3. Otherwise -> False
    """
    if settings is None:
        settings = get_settings()

    if os.environ.get("FORCE_USE_MOCK", "").lower() in ("1", "true", "yes"):
        return True

    if not os.environ.get("SERPAPI_API_KEY") and not os.environ.get("TAVILY_API_KEY"):
        return True

    return False


def use_mock_llm(settings=None) -> bool:
    """Return True when LLM should default to mock.

    Priority:
    - If `FORCE_USE_MOCK` set -> True
    - If `MODEL_NAME` is missing or starts with 'mock' -> True
    - Else False
    """
    if settings is None:
        settings = get_settings()

    if os.environ.get("FORCE_USE_MOCK", "").lower() in ("1", "true", "yes"):
        return True

    name = getattr(settings, "model_name", None)
    if not name:
        return True
    if str(name).lower().startswith("mock"):
        return True
    return False
