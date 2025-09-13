import pytest
from research_agent_framework.mcp.tools import ToolRegistry
from research_agent_framework.logging import LoguruLogger

def dummy_tool(x):
    """Returns x squared."""
    return x * x

def another_tool(y):
    """Returns y plus 10."""
    return y + 10

@pytest.fixture
def registry():
    logger = LoguruLogger()
    return ToolRegistry(logger)

def test_register_and_list_tools(registry):
    registry.register("square", dummy_tool)
    registry.register("plus_ten", another_tool)
    tools = registry.list_tools()
    assert "square" in tools
    assert "plus_ten" in tools
    assert tools["square"](3) == 9
    assert tools["plus_ten"](5) == 15

def test_describe_tools(registry):
    registry.register("square", dummy_tool)
    registry.register("plus_ten", another_tool)
    desc = registry.describe_tools()
    assert desc["square"] == "Returns x squared."
    assert desc["plus_ten"] == "Returns y plus 10."
