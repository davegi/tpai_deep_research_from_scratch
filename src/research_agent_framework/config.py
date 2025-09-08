"""Configuration for research_agent_framework.

Provides a Pydantic v2 `Settings` model (pydantic-settings) that is driven by environment variables. Includes a small `get_settings()` cache
helper.

Assumptions: - pydantic v2 is available in the environment used by tests. - Consumers will call `get_settings()` or instantiate `Settings()`
directly.
"""

from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console

# Import logging implementations from logging_impl for clarity and reuse
from research_agent_framework.logging import (
    LoggingProtocol,
    LoguruLogger,
    StdLogger,
)


class LoggingConfig(BaseModel):
    level: str = "INFO"
    fmt: str = "{time} {level} {message}"
    # Holds a logger instance implementing LoggingProtocol
    _logger_impl: Optional[LoggingProtocol] = None

    def get_logger(self, backend: str = "loguru") -> LoggingProtocol:
        if self._logger_impl is not None:
            return self._logger_impl
        if backend == "loguru":
            self._logger_impl = LoguruLogger(level=self.level, fmt=self.fmt)
        elif backend == "std":
            self._logger_impl = StdLogger(level=self.level, fmt=self.fmt)
        else:
            raise ValueError(f"Unsupported backend: {backend}. Supported backends are 'loguru' and 'std'.")
        return self._logger_impl

    def debug(self, msg, *args, **kwargs):
        self.get_logger().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.get_logger().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.get_logger().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.get_logger().error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.get_logger().critical(msg, *args, **kwargs)


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

    # Optional runtime Console instance. Stored on settings so callers can reuse.
    console: Optional[Console] = None

    # Optional logger instance (implements LoggingProtocol)
    logger: Optional[LoggingProtocol] = None

    # Additional flags
    enable_tracing: bool = False
    # Supervisor error handling policy: 'record_and_continue' (default), 'fail_fast'
    supervisor_error_policy: str = "record_and_continue"

    model_config = SettingsConfigDict(
        env_prefix="", 
        frozen=False, 
        arbitrary_types_allowed=True, 
        extra="ignore", 
        env_nested_delimiter="__"
    )

    def __init__(self, **data):
        super().__init__(**data)
        # Ensure console is always initialized
        if self.console is None:
            self.console = Console()
        # Ensure logger is always initialized
        if self.logger is None:
            self.logger = self.logging.get_logger()


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


def get_console(force_reload: bool = False) -> Console:
    """Return a shared rich Console instance from settings, creating it if necessary."""
    s = get_settings(force_reload=force_reload)
    if s.console is None:
        s.console = Console()
    return s.console


def get_logger(force_reload: bool = False, backend: str = "loguru") -> LoggingProtocol:
    """Return a configured logger implementing LoggingProtocol based on the Settings.logging values.

    By default, uses LoguruLogger. Set backend="std" to use StdLogger. Raises ValueError for unsupported backends.
    """
    s = get_settings(force_reload=force_reload)
    if backend not in ("loguru", "std"):
        raise ValueError(f"Unsupported backend: {backend}. Supported backends are 'loguru' and 'std'.")
    return s.logging.get_logger(backend=backend)