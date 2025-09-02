from assertpy import assert_that

def test_import_config_and_get_settings():
    from research_agent_framework import config

    s = config.get_settings()
    assert_that(s).is_not_none()
    assert_that(hasattr(s, "model_name")).is_true()
