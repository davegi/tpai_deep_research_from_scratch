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
    from assertpy import assert_that
    assert_that(tools, description="ToolRegistry should contain 'square'").contains("square")
    assert_that(tools, description="ToolRegistry should contain 'plus_ten'").contains("plus_ten")
    assert_that(tools["square"](3), description="'square' tool should return 9 for input 3").is_equal_to(9)
    assert_that(tools["plus_ten"](5), description="'plus_ten' tool should return 15 for input 5").is_equal_to(15)

def test_describe_tools(registry):
    registry.register("square", dummy_tool)
    registry.register("plus_ten", another_tool)
    desc = registry.describe_tools()
    from assertpy import assert_that
    assert_that(desc["square"], description="Description for 'square' should match docstring").is_equal_to("Returns x squared.")
    assert_that(desc["plus_ten"], description="Description for 'plus_ten' should match docstring").is_equal_to("Returns y plus 10.")
