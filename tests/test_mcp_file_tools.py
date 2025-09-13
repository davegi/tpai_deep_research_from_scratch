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
    assert result == "Hello World!"

def test_read_file_not_found(tmp_path):
    logger = get_logger()
    tool = MCPFileTool(logger)
    result = tool.read_file(str(tmp_path / "missing.txt"))
    assert result is None

def test_read_file_mock_mode():
    logger = get_logger()
    tool = MCPFileTool(logger, mock_mode=True)
    result = tool.read_file("/fake/path/to/file.txt")
    assert result is not None
    assert result.startswith("[MOCK CONTENT]")
    assert "file.txt" in result
