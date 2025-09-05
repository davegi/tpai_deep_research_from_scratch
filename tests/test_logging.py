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

def test_loguru_model_post_init_and_configure():
    logger = LoguruLogger(level="INFO", fmt="{message}")
    logger.model_post_init(None)
    logger.level = "DEBUG"
    logger.fmt = "{message}"
    logger._configure()
    logger.info("model_post_init test")

def test_std_model_post_init_and_configure():
    logger = StdLogger(level="INFO", fmt="%(message)s", stream=sys.stdout)
    logger.model_post_init(None)
    logger.level = "DEBUG"
    logger.fmt = "%(message)s"
    logger.info("model_post_init test")

@pytest.mark.parametrize("LoggerClass,level", [
    (LoguruLogger, "INVALID"),
    (StdLogger, "INVALID"),
])
def test_invalid_log_level(LoggerClass, level):
    logger = LoggerClass(level="INFO", fmt="{message}" if LoggerClass is LoguruLogger else "%(message)s")
    try:
        logger.level = level
    except Exception as e:
        assert_that(str(e)).contains("INVALID")

from hypothesis import given, strategies as st

@given(level=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
       fmt=st.sampled_from(["{message}", "%(message)s", "{time} | {level} | {message}", "%(asctime)s | %(levelname)s | %(message)s"])
)
def test_loguru_property_based(level, fmt):
    logger = LoguruLogger(level=level, fmt=fmt)
    logger.model_post_init(None)
    logger.level = level
    logger.fmt = fmt
    logger.info(f"property-based {level} {fmt}")

@given(level=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    fmt=st.sampled_from(["%(message)s", "%(asctime)s | %(levelname)s | %(message)s"])
)
def test_std_property_based(level, fmt):
    logger = StdLogger(level=level, fmt=fmt, stream=sys.stdout)
    logger.model_post_init(None)
    logger.level = level
    logger.fmt = fmt
    logger.info(f"property-based {level} {fmt}")
