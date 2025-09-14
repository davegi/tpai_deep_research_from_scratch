from dataclasses import dataclass
from typing import Optional

from pydantic_settings import BaseSettings
from rich.console import Console


from research_agent_framework.logging import LoggingProtocol
from research_agent_framework.llm.client import LLMClient
from typing import Protocol

# Define a minimal SearchAdapterProtocol for type safety
class SearchAdapterProtocol(Protocol):
    def search(self, query: str, **kwargs) -> dict:
        ...


@dataclass
class AgentContext:
    """Lightweight container for agent runtime dependencies.

    Prefer passing an `AgentContext` into agents rather than relying on
    module-level globals. Fields are typed for clarity and test safety.
    """
    settings: Optional[BaseSettings] = None
    console: Optional[Console] = None
    logger: Optional[LoggingProtocol] = None
    llm_client: Optional[LLMClient] = None
    search_adapter: Optional[SearchAdapterProtocol] = None

