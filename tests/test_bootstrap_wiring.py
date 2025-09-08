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

    assert c1 is not None
    assert l1 is not None
    # Repeated bootstrap should not replace console/logger instance
    assert c1 is c2
    assert l1 is l2
