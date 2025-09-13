"""
Helpers for comparing LLM prompt and settings effects side-by-side.
- compare_prompts: Run multiple prompts with the same settings, log and return outputs.
- compare_settings: Run a single prompt with multiple settings (e.g., temperature, max_tokens), log and return outputs.
- compare_all: Run all combinations of prompts and settings, log and return outputs.
"""
from typing import List, Dict, Any
from research_agent_framework.llm.client import LLMConfig, llm_factory
from research_agent_framework.config import get_logger
import asyncio

logger = get_logger()

async def compare_prompts(prompts: List[str], config: LLMConfig, provider: str = "mock") -> Dict[str, str]:
    """Run each prompt with the same config, log and return outputs."""
    client = llm_factory(provider, config)
    results = {}
    for prompt in prompts:
        logger.info(f"Comparing prompt: {prompt}")
        output = await client.generate(prompt)
        logger.info(f"Output: {output}")
        results[prompt] = output
    return results

async def compare_settings(prompt: str, configs: List[LLMConfig], provider: str = "mock") -> Dict[str, str]:
    """Run a single prompt with multiple configs, log and return outputs."""
    results = {}
    for config in configs:
        client = llm_factory(provider, config)
        label = f"model={config.model}, temp={config.temperature}, max_tokens={config.max_tokens}"
        logger.info(f"Comparing settings: {label}")
        output = await client.generate(prompt)
        logger.info(f"Output: {output}")
        results[label] = output
    return results

async def compare_all(prompts: List[str], configs: List[LLMConfig], provider: str = "mock") -> Dict[str, Dict[str, str]]:
    """Run all combinations of prompts and configs, log and return outputs."""
    all_results = {}
    for prompt in prompts:
        all_results[prompt] = await compare_settings(prompt, configs, provider)
    return all_results
