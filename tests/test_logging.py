import sys
import pytest
from research_agent_framework.logging import LoguruLogger, StdLogger, LoggingProtocol
from assertpy import assert_that

@pytest.mark.parametrize("LoggerClass,kwargs", [
    (LoguruLogger, {"level": "INFO", "fmt": "{message}"}),
    (StdLogger, {"level": "INFO", "fmt": "%(message)s", "stream": sys.stdout}),
])
def test_logging_protocol_interface(LoggerClass, kwargs, capsys):
    logger: LoggingProtocol = LoggerClass(**kwargs)
    # Test level property
    assert_that(hasattr(logger, "level")).is_true()
    assert_that(logger.level).is_equal_to("INFO")
    logger.level = "WARNING"
    assert_that(logger.level).is_equal_to("WARNING")
    # Test fmt property
    assert_that(hasattr(logger, "fmt")).is_true()
    fmt_val = kwargs["fmt"]
    assert_that(logger.fmt).is_equal_to(fmt_val)
    logger.fmt = fmt_val  # Should not error
    # Test logger property
    assert_that(hasattr(logger, "logger")).is_true()
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
            assert_that(out).contains("stdout test")
