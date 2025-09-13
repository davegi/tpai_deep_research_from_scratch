import os
import json
import pytest
import logging

logger = logging.getLogger("benchmark_test")

@pytest.mark.skipif(
    not os.path.exists(os.path.join(os.path.dirname(__file__), '../notebooks/benchmarks/llm_throughput.json')),
    reason="llm_throughput.json does not exist; run the notebook benchmark cell first."
)
def test_throughput_outputs_are_strings():
    path = os.path.join(os.path.dirname(__file__), '../notebooks/benchmarks/llm_throughput.json')
    logger.info(f"Testing outputs are strings in {path}")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for config, stats in data.items():
        for output in stats['outputs']:
            assert isinstance(output, str), f"Output for {config} is not a string: {output}"
    logger.info("All outputs are strings.")

@pytest.mark.skipif(
    not os.path.exists(os.path.join(os.path.dirname(__file__), '../notebooks/benchmarks/llm_throughput.json')),
    reason="llm_throughput.json does not exist; run the notebook benchmark cell first."
)
def test_throughput_unique_outputs_count():
    path = os.path.join(os.path.dirname(__file__), '../notebooks/benchmarks/llm_throughput.json')
    logger.info(f"Testing unique outputs count in {path}")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for config, stats in data.items():
        unique = set(stats['outputs'])
        assert stats['unique_outputs'] == len(unique), f"Unique outputs count mismatch for {config}"
    logger.info("Unique outputs count matches.")

@pytest.mark.skipif(
    not os.path.exists(os.path.join(os.path.dirname(__file__), '../notebooks/benchmarks/llm_throughput.json')),
    reason="llm_throughput.json does not exist; run the notebook benchmark cell first."
)
def test_throughput_no_coroutine_outputs():
    path = os.path.join(os.path.dirname(__file__), '../notebooks/benchmarks/llm_throughput.json')
    logger.info(f"Testing for coroutine objects in outputs in {path}")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for config, stats in data.items():
        for output in stats['outputs']:
            assert not output.startswith('<coroutine'), f"Coroutine object found in outputs for {config}: {output}"
    logger.info("No coroutine objects found in outputs.")
