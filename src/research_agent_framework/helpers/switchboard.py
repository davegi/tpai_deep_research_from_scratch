"""Helper utilities to determine whether to use mock or live providers.

This centralizes the small environment-driven logic used by the notebook demos
so the behavior can be unit-tested.
"""
import os
from typing import Optional

from research_agent_framework.config import get_settings
from contextlib import contextmanager


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


@contextmanager
def apply_switchboard(force_mock: bool | None = None):
    """Context manager to temporarily apply a centralized switchboard.

    - If `force_mock` is True, sets `FORCE_USE_MOCK=1` in the environment for the
      context duration.
    - If `force_mock` is False, ensures `FORCE_USE_MOCK` is unset for the context.
    - If `force_mock` is None, leaves environment untouched.

    This helper is intentionally small and deterministic so notebook code and
    tests can toggle behavior in one guarded place.
    """
    if force_mock is None:
        # No-op context
        yield
        return

    old = os.environ.get("FORCE_USE_MOCK")
    try:
        if force_mock:
            os.environ["FORCE_USE_MOCK"] = "1"
        else:
            os.environ.pop("FORCE_USE_MOCK", None)
        yield
    finally:
        # Restore previous state
        if old is None:
            os.environ.pop("FORCE_USE_MOCK", None)
        else:
            os.environ["FORCE_USE_MOCK"] = old
