import logging
from rich.logging import RichHandler
from research_agent_framework.config import get_console
from loguru import logger as loguru_logger

def test_rich_handler_std_logging(capsys):
    console = get_console()
    std_logger = logging.getLogger("test_rich_std")
    std_logger.setLevel("INFO")
    std_logger.handlers.clear()
    std_logger.addHandler(RichHandler(console=console, rich_tracebacks=True))
    std_logger.info("[std] Info message")
    std_logger.warning("[std] Warning message")
    # Capture output and check for message presence
    out = capsys.readouterr().out
    from assertpy import assert_that
    assert_that("Info message" in out, description="Std logger output should contain 'Info message'").is_true()
    assert_that("Warning message" in out, description="Std logger output should contain 'Warning message'").is_true()
    # Color codes may not appear in non-terminal test output; skip that assertion

def test_loguru_rich_sink(capsys):
    console = get_console()
    loguru_logger.remove()
    def rich_sink(message):
        record = message.record
        level = record["level"].name
        text = record["message"]
        style_map = {
            "DEBUG": "dim",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "bold red",
            "CRITICAL": "bold white on red",
        }
        style = style_map.get(level, "white")
        console.log(f"[{level}] {text}", style=style)
    loguru_logger.add(rich_sink, level="INFO")
    loguru_logger.info("[loguru] Info message")
    loguru_logger.warning("[loguru] Warning message")
    out = capsys.readouterr().out
    from assertpy import assert_that
    assert_that("Info message" in out, description="Loguru output should contain 'Info message'").is_true()
    assert_that("Warning message" in out, description="Loguru output should contain 'Warning message'").is_true()
    # Color codes may not appear in non-terminal test output; skip that assertion
