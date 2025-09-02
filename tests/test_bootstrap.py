import importlib
import os
import types
import tempfile
import sys
import types
import pytest

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
    assert called['env']
    assert called['rich']
    assert called['remove']
    assert called['add'] == (print, "DEBUG", "fmt")

    # Second call should do nothing
    called.clear()
    bs.bootstrap()
    assert not called  # No new calls

    # Force should re-run
    bs.bootstrap(force=True)
    assert called['env']
    assert called['rich']
    assert called['remove']
    assert called['add'] == (print, "DEBUG", "fmt")

import subprocess
import sys
import textwrap
import os

def test_bootstrap_env_read(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text("MODEL_NAME=from-env\n")

    script = textwrap.dedent(f"""
        import os
        os.chdir({repr(str(tmp_path))})
        import sys
        sys.path.insert(0, {repr(os.path.abspath('src'))})
        from research_agent_framework.bootstrap import bootstrap
        bootstrap(force=True)
        from research_agent_framework.config import get_settings
        print(get_settings(force_reload=True).model_name)
    """)

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": os.path.abspath("src"), "ENV_PATH": str(env_path)},
    )
    assert result.returncode == 0, f"Subprocess failed: {result.stderr}"
    assert result.stdout.strip() == "from-env"
