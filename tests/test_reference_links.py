"""
Test reference links logging helper for documentation and best practices.
"""
from research_agent_framework.reference_links import log_reference_links

def test_log_reference_links(caplog):
    log_reference_links()
    assert 'See LangChain docs for tracing setup' in caplog.text
    assert 'See Pydantic settings docs' in caplog.text
    assert 'See Rich logging docs' in caplog.text
    assert 'See Loguru logging docs' in caplog.text
    assert 'See Pytest best practices' in caplog.text
