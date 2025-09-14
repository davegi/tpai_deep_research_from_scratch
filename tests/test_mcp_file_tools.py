import pytest
import os
from research_agent_framework.mcp.file_tools import MCPFileTool
from research_agent_framework.config import get_logger

def test_read_file_success(tmp_path):
    logger = get_logger()
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello World!", encoding="utf-8")
    tool = MCPFileTool(logger)
    result = tool.read_file(str(file_path))
    from assertpy import assert_that
    assert_that(result, description="File read should return correct content").is_equal_to("Hello World!")

def test_read_file_not_found(tmp_path):
    logger = get_logger()
    tool = MCPFileTool(logger)
    result = tool.read_file(str(tmp_path / "missing.txt"))
    from assertpy import assert_that
    assert_that(result, description="File read should return None for missing file").is_none()

def test_read_file_mock_mode():
    logger = get_logger()
    tool = MCPFileTool(logger, mock_mode=True)
    result = tool.read_file("/fake/path/to/file.txt")
    from assertpy import assert_that
    assert_that(result, description="Mock mode should return non-None content").is_not_none()
    assert_that(result, description="Mock mode should return content starting with '[MOCK CONTENT]'").starts_with("[MOCK CONTENT]")
    assert_that(result, description="Mock mode content should contain filename").contains("file.txt")
