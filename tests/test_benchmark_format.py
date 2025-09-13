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
    assert out_file.exists(), f'Expected benchmark JSON at {out_file}'
    # ensure parsable
    import json
    data = json.loads(out_file.read_text(encoding='utf-8'))
    assert isinstance(data, dict)
    assert 'mock' in data or 'simulated_live' in data
