"""
Test troubleshooting helpers for setup issues and logging in research_agent_framework.
"""
import os
import pytest
from research_agent_framework.troubleshooting import (
    log_env_reload, log_import_error, log_rich_logging_enabled,
    log_adapter_key_missing, log_kernel_restart, check_adapter_keys
)

def test_log_env_reload():
    os.environ['MODEL_NAME'] = 'mock-model-test'
    settings = log_env_reload()
    from assertpy import assert_that
    assert_that(settings.model_name, description="log_env_reload should set model_name to 'mock-model-test'").is_equal_to('mock-model-test')

def test_log_import_error(caplog):
    log_import_error()
    from assertpy import assert_that
    assert_that(any('Import error' in r for r in caplog.text.splitlines()), description="Log should contain 'Import error'").is_true()

def test_log_rich_logging_enabled(caplog):
    log_rich_logging_enabled()
    from assertpy import assert_that
    assert_that(any('Rich logging enabled' in r for r in caplog.text.splitlines()), description="Log should contain 'Rich logging enabled'").is_true()

def test_log_adapter_key_missing(caplog):
    log_adapter_key_missing('SERPAPI')
    from assertpy import assert_that
    assert_that(any('Adapter API key missing' in r for r in caplog.text.splitlines()), description="Log should contain 'Adapter API key missing'").is_true()

def test_log_kernel_restart(caplog):
    log_kernel_restart()
    from assertpy import assert_that
    assert_that(any('Kernel restarted' in r for r in caplog.text.splitlines()), description="Log should contain 'Kernel restarted'").is_true()

def test_check_adapter_keys(monkeypatch, caplog):
    monkeypatch.delenv('SERPAPI_API_KEY', raising=False)
    monkeypatch.delenv('TAVILY_API_KEY', raising=False)
    serpapi, tavily = check_adapter_keys()
    from assertpy import assert_that
    assert_that(serpapi is None and tavily is None, description="Both adapter keys should be None when not set").is_true()
    assert_that('Adapter API key missing for SERPAPI' in caplog.text, description="Log should contain missing SERPAPI key message").is_true()
    assert_that('Adapter API key missing for TAVILY' in caplog.text, description="Log should contain missing TAVILY key message").is_true()
