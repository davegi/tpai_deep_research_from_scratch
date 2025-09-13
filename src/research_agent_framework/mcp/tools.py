"""
Tool registry and discovery for MCP stub. Used for educational notebook and tests.
"""
from typing import Dict, Any, Callable
from research_agent_framework.logging import LoggingProtocol

class ToolRegistry:
    def __init__(self, logger: LoggingProtocol):
        self.logger = logger
        self.tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]):
        self.logger.info(f"Registering tool: {name}")
        self.tools[name] = func

    def list_tools(self) -> Dict[str, Callable[..., Any]]:
        self.logger.info(f"Listing {len(self.tools)} registered tools.")
        return self.tools.copy()

    def describe_tools(self) -> Dict[str, str]:
        desc = {}
        for name, func in self.tools.items():
            doc = func.__doc__ or "No docstring provided."
            desc[name] = doc.strip()
            self.logger.info(f"Tool: {name} - {doc}")
        return desc
