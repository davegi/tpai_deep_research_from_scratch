"""
Troubleshooting helpers for common setup issues in research_agent_framework.
Provides logging and diagnostic functions for environment, imports, adapters, and notebook kernel issues.
"""
from research_agent_framework.config import get_logger, get_settings
import os

def log_env_reload():
    logger = get_logger(backend='std')
    msg = 'Environment reloaded.'
    logger.info(msg)
    return get_settings(force_reload=True)

def log_import_error():
    logger = get_logger(backend='std')
    msg = 'Import error: src not found on sys.path.'
    logger.error(msg)

def log_rich_logging_enabled():
    logger = get_logger(backend='std')
    logger.info('Rich logging enabled.')

def log_adapter_key_missing(adapter_name):
    logger = get_logger(backend='std')
    msg = f'Adapter API key missing for {adapter_name}; using mock adapter.'
    logger.warning(msg)

def log_kernel_restart():
    logger = get_logger(backend='std')
    msg = 'Kernel restarted.'
    logger.info(msg)

def check_adapter_keys():
    serpapi = os.environ.get('SERPAPI_API_KEY')
    tavily = os.environ.get('TAVILY_API_KEY')
    logger = get_logger()
    if not serpapi:
        log_adapter_key_missing('SERPAPI')
    if not tavily:
        log_adapter_key_missing('TAVILY')
    return serpapi, tavily
