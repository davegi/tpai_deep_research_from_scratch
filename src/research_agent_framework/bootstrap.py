"""Bootstrap helper for research_agent_framework.

Provides `bootstrap()` which: - reads a `.env` file via `environs.Env().read_env()` if available - installs `rich.traceback` for pretty
tracebacks - configures `loguru` with settings from `config.get_settings()`

The function is idempotent and safe to call multiple times.
"""
import threading
from typing import Optional

from environs import Env
from loguru import logger as _logger
from rich import traceback as _rich_traceback

from .config import get_settings

# Keep a simple module-level lock and flag for idempotence
_bootstrap_lock = threading.Lock()
_bootstrapped = False


def bootstrap(force: bool = False) -> None:
    """Run environment bootstrap and logging configuration.

    This simplified bootstrap assumes `environs`, `loguru`, and `rich` are available.
    It's idempotent and will re-run only when `force=True`.
    """
    global _bootstrapped
    with _bootstrap_lock:
        if _bootstrapped and not force:
            return

        # Read .env via environs (will raise if .env parsing fails)
        env = Env()
        import os
        env_path = os.environ.get("ENV_PATH")
        if env_path:
            env.read_env(env_path)
        else:
            env.read_env()

        # Install rich traceback
        _rich_traceback.install()

        # Configure loguru logger
        settings = get_settings()
        _logger.remove()
        _logger.add(sink=print, level=settings.logging.level, format=settings.logging.fmt)

        _bootstrapped = True
