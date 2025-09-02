import sys

import pytest
import sys
import logging
from research_agent_framework.logging import LoguruLogger, StdLogger, LoggingProtocol

@pytest.mark.parametrize("LoggerClass,kwargs", [
    (LoguruLogger, {"level": "INFO", "fmt": "{message}"}),
    (StdLogger, {"level": "INFO", "fmt": "%(message)s", "stream": sys.stdout}),
])
def test_logging_protocol_interface(LoggerClass, kwargs, capsys):
    logger: LoggingProtocol = LoggerClass(**kwargs)
    # Test level property
    assert hasattr(logger, "level")
    assert logger.level == "INFO"
    logger.level = "WARNING"
    assert logger.level == "WARNING"
    # Test fmt property
    assert hasattr(logger, "fmt")
    fmt_val = kwargs["fmt"]
    assert logger.fmt == fmt_val
    logger.fmt = fmt_val  # Should not error
    # Test logger property
    assert hasattr(logger, "logger")
    # Test logging methods (should not raise)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    # Optionally, check output for StdLogger
    if isinstance(logger, StdLogger):
        logger.level = "INFO"
        logger.info("stdout test")
        # Only check output if the logger's stream is sys.stdout or sys.stderr
        stream = getattr(logger.logger, 'stream', None)
        if stream in (sys.stdout, sys.stderr):
            out, _ = capsys.readouterr()
            assert "stdout test" in out
