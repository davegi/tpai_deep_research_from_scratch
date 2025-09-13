"""Notebook bootstrap helper.

This module provides a single function `ensure_src_and_bootstrap()` intended for use
at the top of educational notebooks in this repo. It ensures the local `src` or
repository root is on `sys.path`, sets `PYTHONPATH` when appropriate, then calls
the project's `bootstrap()` function and returns common handles: (settings, console, logger).

Keep this file lightweight and safe to import multiple times.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional, Tuple


def _find_repo_src(start: Optional[Path] = None) -> Optional[Path]:
    """Search upwards from `start` (or cwd) for a folder containing
    `src/research_agent_framework` or `research_agent_framework`. Return the
    `src` path if found, otherwise the repository root path.
    """
    repo_cwd = (start or Path.cwd()).resolve()
    for candidate in [repo_cwd] + list(repo_cwd.parents):
        if (candidate / "src" / "research_agent_framework").exists():
            return (candidate / "src").resolve()
        if (candidate / "research_agent_framework").exists():
            return candidate.resolve()
    return None


def ensure_src_and_bootstrap(start: Optional[Path] = None):
    """Ensure local `src` (or repo root) is on `sys.path`, call project bootstrap,
    and return (settings, console, logger) for notebooks to use.

    The function is idempotent and safe to call multiple times.
    """
    found_src = _find_repo_src(start=start)
    if found_src is not None:
        src_path = str(found_src)
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
            # Set PYTHONPATH for spawned kernels/environments that inspect it
            os.environ.setdefault("PYTHONPATH", src_path)

    # Import project bootstrap and helpers lazily so this module can be imported
    # even when the project is not installed (during static analysis).
    try:
        from research_agent_framework.bootstrap import bootstrap
        from research_agent_framework.config import get_settings, get_console, get_logger
    except Exception:
        # Re-raise with context to help debugging in notebooks
        raise

    # Run bootstrap (idempotent) and return commonly used handles
    bootstrap()
    settings = get_settings()
    console = get_console()
    logger = get_logger()
    return settings, console, logger

