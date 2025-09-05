"""Bootstrap helper for research_agent_framework.

Provides `bootstrap()` which: - reads a `.env` file via `environs.Env().read_env()` if available - installs `rich.traceback` for pretty
tracebacks - configures `loguru` with settings from `config.get_settings()`

The function is idempotent and safe to call multiple times.
"""
import threading
from typing import Optional

from assertpy import assert_that
from environs import Env
from loguru import logger as _logger
from rich import traceback as _rich_traceback
from rich.console import Console

from .config import get_settings

# Keep a simple module-level lock and flag for idempotence
_bootstrap_lock = threading.Lock()
_bootstrapped = False
# Exportable console and logger for other modules to import
console: Optional[Console] = None
logger = _logger


def bootstrap(force: bool = False) -> None:
    """Run environment bootstrap and logging configuration.

    This simplified bootstrap assumes `environs`, `loguru`, and `rich` are available.
    It's idempotent and will re-run only when `force=True`.
    """
    global _bootstrapped, console, logger
    with _bootstrap_lock:
        if _bootstrapped and not force:
            return

        # Read .env via environs (will raise if .env parsing fails)
        env = Env()
        import os
        env_path = os.environ.get("ENV_PATH")
        try:
            if env_path:
                env.read_env(env_path)
            else:
                env.read_env()
        except FileNotFoundError:
            pass

        # Install rich traceback
        _rich_traceback.install()

        # Create a shared rich Console for the application (exported as `console`)
        c = Console()
        console = c
        assert_that(console).is_not_none()

        # Configure loguru logger to write to the rich Console (preserving formatting)
        settings = get_settings()
        _logger.remove()

        # Use the local Console instance as the sink target. Convert the incoming message to str
        # because loguru may pass rich objects.
        _logger.add(lambda m: c.print(str(m), end=""), level=settings.logging.level, format=settings.logging.fmt)

        _bootstrapped = True

    # expose module-level logger alias
    logger = _logger
