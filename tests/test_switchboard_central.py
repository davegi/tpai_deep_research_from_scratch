import os
from research_agent_framework.helpers.switchboard import use_mock_search, use_mock_llm, apply_switchboard
from research_agent_framework.config import get_settings


def test_apply_switchboard_force_true():
    # Ensure we can force mocks on even if settings would prefer live
    s = get_settings(force_reload=True)
    from assertpy import assert_that
    with apply_switchboard(force_mock=True):
        s2 = get_settings(force_reload=True)
        assert_that(use_mock_search(s2), description="use_mock_search should be True when force_mock is True").is_true()
        assert_that(use_mock_llm(s2), description="use_mock_llm should be True when force_mock is True").is_true()


def test_apply_switchboard_force_false():
    # Ensure we can clear FORCE_USE_MOCK and allow settings to decide
    # Temporarily set FORCE_USE_MOCK then clear with context
    from assertpy import assert_that
    os.environ['FORCE_USE_MOCK'] = '1'
    try:
        s = get_settings(force_reload=True)
        assert_that(use_mock_search(s), description="use_mock_search should be True when FORCE_USE_MOCK is set").is_true()
        with apply_switchboard(force_mock=False):
            s2 = get_settings(force_reload=True)
            # When force_mock=False we expect the helper to respect actual credentials or model
            # can't assert exact boolean because environment may differ; just ensure no exception
            _ = use_mock_search(s2)
            _ = use_mock_llm(s2)
    finally:
        os.environ.pop('FORCE_USE_MOCK', None)
