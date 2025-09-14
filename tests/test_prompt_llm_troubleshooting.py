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
    from assertpy import assert_that
    assert_that('Prompt ambiguity detected' in caplog.text, description="Log should contain 'Prompt ambiguity detected'").is_true()

def test_log_temperature_setting(caplog):
    log_temperature_setting()
    from assertpy import assert_that
    assert_that('Temperature set to' in caplog.text, description="Log should contain 'Temperature set to'").is_true()

def test_log_output_truncated(caplog):
    log_output_truncated()
    from assertpy import assert_that
    assert_that('Output truncated' in caplog.text, description="Log should contain 'Output truncated'").is_true()

def test_log_provider_model_mismatch(caplog):
    log_provider_model_mismatch()
    from assertpy import assert_that
    assert_that('Provider/model mismatch' in caplog.text, description="Log should contain 'Provider/model mismatch'").is_true()

def test_log_prompt_config_output(caplog):
    log_prompt_config_output('Test prompt', {'temp': 0.5}, 'Test output')
    from assertpy import assert_that
    assert_that('Prompt: Test prompt' in caplog.text, description="Log should contain 'Prompt: Test prompt'").is_true()
    assert_that("Config: {'temp': 0.5}" in caplog.text, description="Log should contain 'Config: {\'temp\': 0.5}'").is_true()
    assert_that('Output: Test output' in caplog.text, description="Log should contain 'Output: Test output'").is_true()
