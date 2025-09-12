"""Bootstrap helper for research_agent_framework.

`bootstrap()` performs early environment and logging setup:
- reads a `.env` file via `environs.Env().read_env()` if available
- installs `rich.traceback` for pretty tracebacks
- ensures a shared `Console` exists via `get_settings().console`
- wires global Loguru logger to the Console using current settings

The function is idempotent and safe to call multiple times; pass `force=True`
to re-run wiring.
"""
import threading
from typing import cast

from assertpy import assert_that
from environs import Env
from loguru import logger as _logger
from rich import traceback as _rich_traceback
from rich.console import Console

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
        try:
            if env_path:
                env.read_env(env_path)
            else:
                env.read_env()
        except Exception:
            pass

        # Install rich traceback
        _rich_traceback.install()

        # Ensure shared Console exists via settings property; tolerate missing attribute in tests
        settings = get_settings()
        try:
            c = settings.console
        except AttributeError:
            # Create and attach a Console dynamically if tests provide a minimal DummySettings
            c = Console()
            try:
                setattr(settings, "console", c)
            except Exception:
                pass
        assert_that(c).is_not_none()
        c = cast(Console, c)

        # Configure std logging to use RichHandler
        import logging
        from rich.logging import RichHandler
        std_fmt = '%(asctime)s %(levelname)s %(message)s'
        logging.basicConfig(
            level=settings.logging.level,
            format=std_fmt,
            handlers=[RichHandler(console=c, rich_tracebacks=True)]
        )

        # Configure loguru logger to use Console.log for colorized output
        _logger.remove()
        def rich_loguru_sink(message):
            record = message.record
            level = record["level"].name
            text = record["message"]
            # Use style based on log level
            style_map = {
                "DEBUG": "dim",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "bold red",
                "CRITICAL": "bold white on red",
            }
            style = style_map.get(level, "white")
            c.log(f"[{level}] {text}", style=style)
        _logger.add(rich_loguru_sink, level=settings.logging.level, format=settings.logging.fmt)

        _bootstrapped = True
        _logger.add(rich_loguru_sink, level=settings.logging.level, format=settings.logging.fmt)

        _bootstrapped = True
