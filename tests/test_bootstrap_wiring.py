def test_bootstrap_wiring_idempotent_and_console_logger():
    # Import here to ensure sys.path is set by pytest/test harness
    from research_agent_framework import bootstrap
    from research_agent_framework.config import get_console, get_logger, get_settings

    # Run bootstrap multiple times to confirm idempotence and wiring
    bootstrap.bootstrap(force=True)
    c1 = get_console()
    l1 = get_logger()

    bootstrap.bootstrap(force=True)
    c2 = get_console()
    l2 = get_logger()

    from assertpy import assert_that
    assert_that(c1).is_not_none()
    assert_that(l1).is_not_none()
    # Repeated bootstrap should not replace console/logger instance
    assert_that(c1 is c2).is_true()
    assert_that(l1 is l2).is_true()
