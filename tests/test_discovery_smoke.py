def test_import_config_and_get_settings():
    from research_agent_framework import config

    s = config.get_settings()
    assert s is not None
    assert hasattr(s, "model_name")
