import importlib
import os
import types
from copy import deepcopy
from assertpy import assert_that


def test_settings_defaults():
    cfg = importlib.import_module("research_agent_framework.config")
    s = cfg.Settings()
    assert_that(s.model_name).is_equal_to("mock-model")
    assert_that(s.model_temperature).is_instance_of(float)
    assert_that(s.enable_tracing).is_false()


def test_get_settings_caching_and_force_reload(monkeypatch, tmp_path):
    cfg = importlib.import_module("research_agent_framework.config")
    # ensure a fresh cache by setting _settings to None
    _orig = getattr(cfg, "_settings", None)
    try:
        setattr(cfg, "_settings", None)

        s1 = cfg.get_settings()
        # mutate returned object and ensure subsequent call returns same object
        s1.model_name = "changed"
        s2 = cfg.get_settings()
        assert_that(s1).is_same_as(s2)
        assert_that(s2.model_name).is_equal_to("changed")

        # force reload should return a new instance
        s3 = cfg.get_settings(force_reload=True)
        assert_that(s3).is_not_same_as(s2)
    finally:
        setattr(cfg, "_settings", _orig)


def test_env_overrides(monkeypatch):
    cfg = importlib.import_module("research_agent_framework.config")
    # set env vars for pydantic Settings
    monkeypatch.setenv("MODEL_NAME", "env-model")
    monkeypatch.setenv("MODEL_TEMPERATURE", "0.7")
    s = cfg.Settings()
    assert_that(s.model_name).is_equal_to("env-model")
    assert_that(s.model_temperature).is_close_to(0.7, 1e-6)


def test_invalid_type_raises():
    cfg = importlib.import_module("research_agent_framework.config")
    # Passing wrong type to model_temperature should raise ValidationError
    try:
        cfg.Settings(model_temperature="not-a-float")
        raised = False
    except Exception:
        raised = True
    assert_that(raised).is_true()



# --- Logging Protocol Test Grouping ---
import pytest

class TestLoggingProtocol:
    def test_logging_property_returns_logging_config(self):
        cfg = importlib.import_module("research_agent_framework.config")
        s = cfg.Settings(logging=cfg.LoggingConfig(level="DEBUG", fmt="fmt"))
        logging_cfg = s.logging
        assert_that(hasattr(logging_cfg, "level")).is_true()
        assert_that(logging_cfg.level).is_equal_to("DEBUG")
        assert_that(logging_cfg.fmt).is_equal_to("fmt")
        # Test logger interface
        logger = logging_cfg.get_logger()
        assert_that(hasattr(logger, "info")).is_true()
        assert_that(hasattr(logger, "debug")).is_true()
        logger.info("test info message")
        logger.debug("test debug message")

    class TestLoguruLogger:
        def test_loguru_logger_interface(self):
            cfg = importlib.import_module("research_agent_framework.config")
            LoguruLogger = cfg.LoguruLogger
            logger = LoguruLogger(level="INFO", fmt="{message}")
            assert_that(logger.level).is_equal_to("INFO")
            logger.level = "DEBUG"
            assert_that(logger.level).is_equal_to("DEBUG")
            logger.info("info message")
            logger.debug("debug message")
            logger.warning("warning message")
            logger.error("error message")
            logger.critical("critical message")

    class TestStdLogger:
        def test_std_logger_interface(self):
            cfg = importlib.import_module("research_agent_framework.config")
            StdLogger = cfg.StdLogger
            logger = StdLogger(level="INFO", fmt="%(message)s")
            assert_that(logger.level).is_equal_to("INFO")
            logger.level = "WARNING"
            assert_that(logger.level).is_equal_to("WARNING")
            logger.info("info message")
            logger.debug("debug message")
            logger.warning("warning message")
            logger.error("error message")
            logger.critical("critical message")


def test_logging_env_nested(monkeypatch):
    cfg = importlib.import_module("research_agent_framework.config")
    monkeypatch.setenv("LOGGING__LEVEL", "WARNING")
    monkeypatch.setenv("LOGGING__FMT", "{message}")
    s = cfg.Settings()
    assert_that(s.logging.level).is_equal_to("WARNING")
    assert_that(s.logging.fmt).is_equal_to("{message}")
