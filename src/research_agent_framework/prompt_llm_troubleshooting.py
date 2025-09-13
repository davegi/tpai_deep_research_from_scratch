"""
Prompt/LLM troubleshooting helpers for common pitfalls and mitigations.
Provides logging and diagnostic functions for prompt clarity, temperature, max_tokens, and provider/model issues.
"""
from research_agent_framework.config import get_logger, get_settings

def log_prompt_ambiguity():
    logger = get_logger(backend='std')
    msg = 'Prompt ambiguity detected; refining prompt.'
    logger.warning(msg)

def log_temperature_setting():
    settings = get_settings()
    logger = get_logger(backend='std')
    msg = f'Temperature set to {settings.model_temperature}'
    logger.info(msg)

def log_output_truncated():
    logger = get_logger(backend='std')
    msg = 'Output truncated; consider increasing max_tokens.'
    logger.warning(msg)

def log_provider_model_mismatch():
    logger = get_logger(backend='std')
    msg = 'Provider/model mismatch; using mock LLM.'
    logger.error(msg)

def log_prompt_config_output(prompt, config, output):
    logger = get_logger(backend='std')
    msg = f'Prompt: {prompt}\nConfig: {config}\nOutput: {output}'
    logger.info(msg)
