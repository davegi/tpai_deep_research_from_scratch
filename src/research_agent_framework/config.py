"""Configuration for research_agent_framework.

Provides a Pydantic v2 `Settings` model (pydantic-settings) that is driven by environment variables. Includes a small `get_settings()` cache
helper.

Assumptions: - pydantic v2 is available in the environment used by tests. - Consumers will call `get_settings()` or instantiate `Settings()`
directly.
"""
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingConfig(BaseModel):
    level: str = "INFO"
    fmt: str = "{time} {level} {message}"

    model_config = SettingsConfigDict(populate_by_name=True)


class Settings(BaseSettings):
    """Application settings loaded from environment.

    Fields use environment variable names that are the uppercase form of the attribute (Pydantic Settings default behavior). Supports nested
    logging config via LOGGING__LEVEL and LOGGING__FMT.
    """

    model_name: str = "mock-model"
    model_temperature: float = 0.0
    llm_endpoint: Optional[str] = None
    llm_api_key: Optional[str] = None

    # Nested logging config
    logging: LoggingConfig = LoggingConfig()

    # Additional flags
    enable_tracing: bool = False

    model_config = SettingsConfigDict(env_prefix="", frozen=False, arbitrary_types_allowed=True, extra="ignore", env_nested_delimiter="__")

# simple module-level cache
_settings: Optional[Settings] = None


def get_settings(force_reload: bool = False) -> Settings:
    """Return cached Settings instance. Set force_reload=True to re-read env.

    Simpler implementation: maintain a module-level cache and recreate Settings when force_reload is True or when cache is empty.
    """
    global _settings
    if _settings is None or force_reload:
        # Remove cached settings and force pydantic to re-read environment
        import importlib
        import sys
        # Remove Settings from pydantic cache if present
        if "research_agent_framework.config" in sys.modules:
            importlib.reload(sys.modules["research_agent_framework.config"])
        _settings = Settings()
    return _settings
