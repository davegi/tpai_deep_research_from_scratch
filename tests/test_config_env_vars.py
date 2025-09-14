import os

from research_agent_framework.config import get_settings


def test_get_settings_reads_env_var(tmp_path, monkeypatch):
    # Ensure a clean environment and then set a test env var
    monkeypatch.delenv("MODEL_NAME", raising=False)
    monkeypatch.setenv("MODEL_NAME", "test-model-from-env")

    s = get_settings(force_reload=True)
    from assertpy import assert_that
    assert_that(s.model_name, description="MODEL_NAME env var should be read by get_settings").is_equal_to("test-model-from-env")
