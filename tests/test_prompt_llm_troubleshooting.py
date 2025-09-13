"""
Test prompt/LLM troubleshooting helpers for common pitfalls and mitigations.
"""
import pytest
from research_agent_framework.prompt_llm_troubleshooting import (
    log_prompt_ambiguity, log_temperature_setting, log_output_truncated,
    log_provider_model_mismatch, log_prompt_config_output
)

def test_log_prompt_ambiguity(caplog):
    log_prompt_ambiguity()
    assert 'Prompt ambiguity detected' in caplog.text

def test_log_temperature_setting(caplog):
    log_temperature_setting()
    assert 'Temperature set to' in caplog.text

def test_log_output_truncated(caplog):
    log_output_truncated()
    assert 'Output truncated' in caplog.text

def test_log_provider_model_mismatch(caplog):
    log_provider_model_mismatch()
    assert 'Provider/model mismatch' in caplog.text

def test_log_prompt_config_output(caplog):
    log_prompt_config_output('Test prompt', {'temp': 0.5}, 'Test output')
    assert 'Prompt: Test prompt' in caplog.text
    assert 'Config: {\'temp\': 0.5}' in caplog.text
    assert 'Output: Test output' in caplog.text
