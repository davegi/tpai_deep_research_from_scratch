import importlib
import os
import types
from copy import deepcopy


def test_settings_defaults():
    cfg = importlib.import_module("research_agent_framework.config")
    s = cfg.Settings()
    assert s.model_name == "mock-model"
    assert isinstance(s.model_temperature, float)
    assert s.enable_tracing is False


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
        assert s1 is s2
        assert s2.model_name == "changed"

        # force reload should return a new instance
        s3 = cfg.get_settings(force_reload=True)
        assert s3 is not s2
    finally:
        setattr(cfg, "_settings", _orig)


def test_env_overrides(monkeypatch):
    cfg = importlib.import_module("research_agent_framework.config")
    # set env vars for pydantic Settings
    monkeypatch.setenv("MODEL_NAME", "env-model")
    monkeypatch.setenv("MODEL_TEMPERATURE", "0.7")
    s = cfg.Settings()
    assert s.model_name == "env-model"
    assert abs(s.model_temperature - 0.7) < 1e-6


def test_invalid_type_raises():
    cfg = importlib.import_module("research_agent_framework.config")
    # Passing wrong type to model_temperature should raise ValidationError
    try:
        cfg.Settings(model_temperature="not-a-float")
        raised = False
    except Exception:
        raised = True
    assert raised



# --- Logging Protocol Test Grouping ---
import pytest

class TestLoggingProtocol:
    def test_logging_property_returns_logging_config(self):
        cfg = importlib.import_module("research_agent_framework.config")
        s = cfg.Settings(logging=cfg.LoggingConfig(level="DEBUG", fmt="fmt"))
        logging_cfg = s.logging
        assert hasattr(logging_cfg, "level")
        assert logging_cfg.level == "DEBUG"
        assert logging_cfg.fmt == "fmt"
        # Test logger interface
        logger = logging_cfg.get_logger()
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")
        logger.info("test info message")
        logger.debug("test debug message")

    class TestLoguruLogger:
        def test_loguru_logger_interface(self):
            cfg = importlib.import_module("research_agent_framework.config")
            LoguruLogger = cfg.LoguruLogger
            logger = LoguruLogger(level="INFO", fmt="{message}")
            assert logger.level == "INFO"
            logger.level = "DEBUG"
            assert logger.level == "DEBUG"
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
            assert logger.level == "INFO"
            logger.level = "WARNING"
            assert logger.level == "WARNING"
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
    assert s.logging.level == "WARNING"
    assert s.logging.fmt == "{message}"
