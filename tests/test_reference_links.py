"""
Test reference links logging helper for documentation and best practices.
"""
from research_agent_framework.reference_links import log_reference_links

def test_log_reference_links(caplog):
    log_reference_links()
    from assertpy import assert_that
    assert_that('See LangChain docs for tracing setup' in caplog.text, description="Log should contain LangChain docs reference").is_true()
    assert_that('See Pydantic settings docs' in caplog.text, description="Log should contain Pydantic docs reference").is_true()
    assert_that('See Rich logging docs' in caplog.text, description="Log should contain Rich logging docs reference").is_true()
    assert_that('See Loguru logging docs' in caplog.text, description="Log should contain Loguru logging docs reference").is_true()
    assert_that('See Pytest best practices' in caplog.text, description="Log should contain Pytest best practices reference").is_true()
