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
    assert settings.model_name == 'mock-model-test'

def test_log_import_error(caplog):
    log_import_error()
    assert any('Import error' in r for r in caplog.text.splitlines())

def test_log_rich_logging_enabled(caplog):
    log_rich_logging_enabled()
    assert any('Rich logging enabled' in r for r in caplog.text.splitlines())

def test_log_adapter_key_missing(caplog):
    log_adapter_key_missing('SERPAPI')
    assert any('Adapter API key missing' in r for r in caplog.text.splitlines())

def test_log_kernel_restart(caplog):
    log_kernel_restart()
    assert any('Kernel restarted' in r for r in caplog.text.splitlines())

def test_check_adapter_keys(monkeypatch, caplog):
    monkeypatch.delenv('SERPAPI_API_KEY', raising=False)
    monkeypatch.delenv('TAVILY_API_KEY', raising=False)
    serpapi, tavily = check_adapter_keys()
    assert serpapi is None and tavily is None
    assert 'Adapter API key missing for SERPAPI' in caplog.text
    assert 'Adapter API key missing for TAVILY' in caplog.text
