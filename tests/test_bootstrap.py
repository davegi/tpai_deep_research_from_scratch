import os
import sys
import types
from assertpy import assert_that

def test_bootstrap_idempotent(monkeypatch):
    # Patch environs.Env.read_env to track calls
    called = {}
    class DummyEnv:
        def read_env(self):
            called['env'] = True
    monkeypatch.setattr("research_agent_framework.bootstrap.Env", DummyEnv)

    # Patch rich.traceback.install
    monkeypatch.setattr("research_agent_framework.bootstrap._rich_traceback.install", lambda: called.setdefault('rich', True))

    # Patch loguru logger
    class DummyLogger:
        def remove(self):
            called['remove'] = True
        def add(self, sink, level, format):
            called['add'] = (sink, level, format)
    monkeypatch.setattr("research_agent_framework.bootstrap._logger", DummyLogger())

    # Patch get_settings
    class DummySettings:
        class logging:
            level = "DEBUG"
            fmt = "fmt"
    monkeypatch.setattr("research_agent_framework.bootstrap.get_settings", lambda: DummySettings())

    # Reset _bootstrapped
    import research_agent_framework.bootstrap as bs
    bs._bootstrapped = False

    # First call should run everything
    bs.bootstrap()
    assert_that(called).contains('env')
    assert_that(called).contains('rich')
    assert_that(called).contains('remove')
    sink, level, fmt = called['add']
    assert_that(callable(sink)).is_true()
    assert_that(level).is_equal_to("DEBUG")
    assert_that(fmt).is_equal_to("fmt")

    # Second call should do nothing
    called.clear()
    bs.bootstrap()
    assert_that(called).is_empty()

    # Force should re-run
    bs.bootstrap(force=True)
    assert_that(called).contains('env')
    assert_that(called).contains('rich')
    assert_that(called).contains('remove')
    sink, level, fmt = called['add']
    assert_that(callable(sink)).is_true()
    assert_that(level).is_equal_to("DEBUG")
    assert_that(fmt).is_equal_to("fmt")

import subprocess
import sys
import textwrap
import os

def test_bootstrap_env_read(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text("MODEL_NAME=from-env\n")

    # --- DO NOT FORMAT THIS BLOCK --- This script string must remain exactly as written for subprocess tests. fmt: off
    script = textwrap.dedent(f"""
import os os.chdir({repr(str(tmp_path))}) import sys sys.path.insert(0, {repr(os.path.abspath('src'))}) from
research_agent_framework.bootstrap import bootstrap bootstrap(force=True) from research_agent_framework.config import get_settings
print(get_settings(force_reload=True).model_name)
    """)
    # fmt: on

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": os.path.abspath("src"), "ENV_PATH": str(env_path)},
    )
    assert_that(result.returncode).is_equal_to(0)
    assert_that(result.stdout.strip()).is_equal_to("from-env")
