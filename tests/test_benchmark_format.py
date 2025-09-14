import os
from pathlib import Path
import pytest

# Conservative test: if benchmarks folder exists, ensure the expected JSON exists and is parsable
def test_benchmark_json_format():
    repo_root = Path(__file__).resolve().parents[1]
    bench_dir = repo_root / 'notebooks' / 'benchmarks'
    if not bench_dir.exists():
        pytest.skip('No benchmark artifacts present; run benchmarks to create them')
    out_file = bench_dir / 'llm_latency.json'
    from assertpy import assert_that
    assert_that(out_file.exists(), description=f"Expected benchmark JSON at {out_file}").is_true()
    # ensure parsable
    import json
    data = json.loads(out_file.read_text(encoding='utf-8'))
    assert_that(data, description="Benchmark JSON should be a dictionary").is_instance_of(dict)
    # Accept either 'mock' or 'simulated_live' key
    assert_that('mock' in data or 'simulated_live' in data, description="Benchmark JSON should contain 'mock' or 'simulated_live' key").is_true()
