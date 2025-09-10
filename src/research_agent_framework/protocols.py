from dataclasses import dataclass
from typing import Any, Optional

from pydantic_settings import BaseSettings
from rich.console import Console

from research_agent_framework.logging import LoggingProtocol


@dataclass
class AgentContext:
    """Lightweight container for agent runtime dependencies.

    Prefer passing an `AgentContext` into agents rather than relying on
    module-level globals. Fields are intentionally permissive to make test
    wiring simple.
    """
    settings: Optional[BaseSettings] = None
    console: Optional[Console] = None
    logger: Optional[LoggingProtocol] = None
    llm_client: Optional[Any] = None
    search_adapter: Optional[Any] = None

