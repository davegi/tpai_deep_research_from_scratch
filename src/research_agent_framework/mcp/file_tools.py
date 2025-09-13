"""
MCP File Tool: Read local docs via MCP tool, with logging and error handling.
Supports deterministic mock fallback for educational notebook and tests.
"""
from typing import Optional
import os
from research_agent_framework.logging import LoggingProtocol

class MCPFileTool:
    def __init__(self, logger: LoggingProtocol, mock_mode: bool = False):
        self.logger = logger
        self.mock_mode = mock_mode

    def read_file(self, path: str) -> Optional[str]:
        self.logger.info(f"MCPFileTool.read_file called with path: {path}")
        if self.mock_mode:
            self.logger.warning("[MOCK MODE] Returning deterministic content.")
            return f"[MOCK CONTENT] File: {os.path.basename(path)}"
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.logger.info(f"Successfully read file: {path}")
            return content
        except FileNotFoundError:
            self.logger.warning(f"[WARNING] File not found: {path}")
            return None
        except Exception as e:
            self.logger.error(f"[ERROR] Exception reading file {path}: {e}")
            return None
