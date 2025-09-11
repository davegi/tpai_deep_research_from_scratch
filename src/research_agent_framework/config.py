"""Configuration for research_agent_framework.

Provides a Pydantic v2 `Settings` model (pydantic-settings) driven by environment variables
and thin helpers to access a shared `Console` and a configured logger via properties.
"""

from typing import Optional, Literal
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
    # Public fields so Pydantic Settings env nesting works (LOGGING__LEVEL, etc.)
    level: str = "INFO"
    fmt: str = "{time} {level} {message}"
    backend: Literal["loguru", "std"] = "loguru"
    # Holds a cached logger instance implementing LoggingProtocol
    _logger_impl: Optional[LoggingProtocol] = None

    @property
    def logger(self) -> LoggingProtocol:
        """Return the cached/default logger, lazily constructed based on backend.

        Uses current `level` and `fmt`. Subsequent changes to `level`/`fmt` are
        applied to the cached implementation.
        """
        if self._logger_impl is None:
            self._logger_impl = self._construct_impl(self.backend)
        # Ensure runtime config is reflected on the impl
        try:
            self._logger_impl.level = self.level
            self._logger_impl.fmt = self.fmt
        except Exception:
            pass
        return self._logger_impl

    def _construct_impl(self, backend: str) -> LoggingProtocol:
        if backend == "loguru":
            return LoguruLogger(level=self.level, fmt=self.fmt)
        if backend == "std":
            return StdLogger(level=self.level, fmt=self.fmt)
        raise ValueError(f"Unsupported backend: {backend}. Supported backends are 'loguru' and 'std'.")

    def get_logger(self, backend: str = "loguru") -> LoggingProtocol:
        """Return a logger for an explicit backend (fresh impl)."""
        return self._construct_impl(backend)

    # Convenience passthrough methods for ergonomic usage
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


class Settings(BaseSettings):
    """Application settings loaded from environment.

    Environment variables follow Pydantic Settings defaults. Nested logging config
    supports LOGGING__LEVEL, LOGGING__FMT, LOGGING__BACKEND.
    """

    model_name: str = "mock-model"
    model_temperature: float = 0.0
    llm_endpoint: Optional[str] = None
    llm_api_key: Optional[str] = None

    # Nested logging config
    logging: LoggingConfig = LoggingConfig()

    # Additional flags
    enable_tracing: bool = False
    # Supervisor error handling policy: 'record_and_continue' (default), 'fail_fast'
    supervisor_error_policy: str = "record_and_continue"

    # Internal, lazily created runtime instances
    _console: Optional[Console] = None

    model_config = SettingsConfigDict(
        env_prefix="",
        frozen=False,
        arbitrary_types_allowed=True,
        extra="ignore",
        env_nested_delimiter="__",
    )

    @property
    def console(self) -> Console:
        if self._console is None:
            self._console = Console()
        return self._console

    @console.setter
    def console(self, value: Console) -> None:
        self._console = value

    @property
    def logger(self) -> LoggingProtocol:
        return self.logging.logger


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
    """Return the shared Console instance.

    Delegates to the property-backed `Settings.console` so all callers share
    the same console instance.
    """
    s = get_settings(force_reload=force_reload)
    return s.console


def get_logger(force_reload: bool = False, backend: Optional[str] = None) -> LoggingProtocol:
    """Return a configured logger.

    If `backend` is None, returns the shared property-backed logger
    (`Settings.logger`). If provided, constructs a fresh logger for that
    backend via `LoggingConfig.get_logger`.
    """
    s = get_settings(force_reload=force_reload)
    if backend is None:
        return s.logger
    if backend not in ("loguru", "std"):
        raise ValueError(f"Unsupported backend: {backend}. Supported backends are 'loguru' and 'std'.")
    return s.logging.get_logger(backend=backend)
