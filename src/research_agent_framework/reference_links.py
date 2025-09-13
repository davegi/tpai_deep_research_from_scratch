"""
Reference links and logging helpers for deeper documentation and best practices.
"""
from research_agent_framework.config import get_logger

def log_reference_links():
    logger = get_logger()
    logger.info('See LangChain docs for tracing setup: https://docs.langchain.com/docs/langsmith')
    logger.info('See Pydantic settings docs: https://docs.pydantic.dev/latest/concepts/settings/')
    logger = get_logger(backend='std')
    logger.info('See LangChain docs for tracing setup: https://docs.langchain.com/docs/langsmith')
    logger.info('See Pydantic settings docs: https://docs.pydantic.dev/latest/concepts/settings/')
    logger.info('See Rich logging docs: https://rich.readthedocs.io/en/stable/logging.html')
    logger.info('See Loguru logging docs: https://loguru.readthedocs.io/en/stable/')
    logger.info('See Pytest best practices: https://docs.pytest.org/en/stable/how-to/best-practices.html')
