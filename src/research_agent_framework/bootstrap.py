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

from .config import get_settings, get_console, get_logger

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

        # Create or reuse the shared Console for the application (tests patch this via bootstrap.Console)
        settings = get_settings()
        # If force=True we should recreate the Console using the module-level
        # `Console` constructor so tests that monkeypatch that constructor are
        # exercised. Otherwise prefer an existing module-level console, then
        # settings.console, and finally construct a new Console.
        if force:
            # Re-run bootstrap actions. Recreate the Console only when:
            # - there is no existing module-level console, or
            # - the existing console is NOT an instance of the currently-imported
            #   `Console` class (this ensures tests that monkeypatch
            #   `bootstrap.Console` get exercised),
            # otherwise reuse the existing console to preserve idempotence.
            try:
                if console is not None and isinstance(console, Console):
                    c = console
                else:
                    c = Console()
            except Exception:
                # fall back to any existing console or settings.console if constructor fails
                c = console
                try:
                    existing = getattr(settings, "console", None)
                    if c is None and existing is not None:
                        c = existing
                except Exception:
                    pass
        else:
            if console is not None:
                c = console
            else:
                try:
                    existing = getattr(settings, "console", None)
                except Exception:
                    existing = None
                if existing is not None:
                    c = existing
                else:
                    c = Console()
        console = c
        # Also make sure Settings holds a reference so get_console() and consumers reuse it
        try:
            settings.console = c
        except Exception:
            pass

        assert_that(console).is_not_none()
        # Help type-checkers: `c` must be a Console here.
        assert c is not None

        # Configure loguru logger to write to the shared Console (preserving formatting)
        _logger.remove()
        # Use the shared Console as the sink target. Convert the incoming message to str
        # because loguru may pass rich objects.
        _logger.add(lambda m: c.print(str(m), end=""), level=settings.logging.level, format=settings.logging.fmt)

        _bootstrapped = True

    # expose module-level logger alias
    logger = _logger
