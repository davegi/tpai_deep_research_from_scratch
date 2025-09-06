import os
import sys
import textwrap
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from unittest.mock import patch
from assertpy import assert_that


def test_bootstrap_missing_env(monkeypatch):
    # Patch environs.Env.read_env to raise FileNotFoundError
    class DummyEnv:
        def read_env(self):
            raise FileNotFoundError(".env not found")

    monkeypatch.setattr("research_agent_framework.bootstrap.Env", DummyEnv)
    monkeypatch.setattr("research_agent_framework.bootstrap._rich_traceback.install", lambda: None)
    monkeypatch.setattr(
        "research_agent_framework.bootstrap._logger",
        type("DummyLogger", (), {"remove": lambda self: None, "add": lambda self, sink, level, format: None})(),
    )
    monkeypatch.setattr(
        "research_agent_framework.bootstrap.get_settings",
        lambda: type("DummySettings", (), {"logging": type("DummyLogging", (), {"level": "INFO", "fmt": "fmt"})()})(),
    )
    import research_agent_framework.bootstrap as bs

    bs._bootstrapped = False
    # Should not raise, just skip .env
    bs.bootstrap(force=True)


def test_bootstrap_console_and_logger(monkeypatch):
    # Patch Console and logger creation and ensure bootstrap wires them up
    created = {}

    class DummyConsole:
        def __init__(self):
            created["console"] = True

        def print(self, msg, end=None):
            pass

    class DummyLogger:
        def remove(self):
            created["remove"] = True

        def add(self, sink, level=None, format=None, *args, **kwargs):
            created["add"] = True

    monkeypatch.setattr("research_agent_framework.bootstrap.Console", DummyConsole)
    monkeypatch.setattr("research_agent_framework.bootstrap._logger", DummyLogger())
    monkeypatch.setattr("research_agent_framework.bootstrap._rich_traceback.install", lambda: None)
    monkeypatch.setattr("research_agent_framework.bootstrap.Env", type("DummyEnv", (), {"read_env": lambda self: None}))
    monkeypatch.setattr(
        "research_agent_framework.bootstrap.get_settings",
        lambda: type("DummySettings", (), {"logging": type("DummyLogging", (), {"level": "INFO", "fmt": "fmt"})()})(),
    )
    import research_agent_framework.bootstrap as bs

    bs._bootstrapped = False
    bs.bootstrap(force=True)
    assert "console" in created
    assert "remove" in created
    assert "add" in created


@given(
    level=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    fmt=st.sampled_from(["{message}", "%(message)s", "{time} | {level} | {message}", "%(asctime)s | %(levelname)s | %(message)s"]),
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_bootstrap_property_based(level, fmt):
    class DummyEnv:
        def read_env(self):
            pass

    class DummyConsole:
        def print(self, msg, end=None):
            pass

    class DummyLogger:
        def remove(self):
            pass

        def add(self, sink, level=None, format=None, *args, **kwargs):
            # level and format should be passed through from settings
            assert format == fmt

    with patch("research_agent_framework.bootstrap.Env", DummyEnv), patch(
        "research_agent_framework.bootstrap.Console", DummyConsole
    ), patch("research_agent_framework.bootstrap._logger", DummyLogger()), patch(
        "research_agent_framework.bootstrap._rich_traceback.install", lambda: None
    ), patch(
        "research_agent_framework.bootstrap.get_settings",
        lambda: type("DummySettings", (), {"logging": type("DummyLogging", (), {"level": level, "fmt": fmt})()})(),
    ):
        import research_agent_framework.bootstrap as bs

        bs._bootstrapped = False
        bs.bootstrap(force=True)


def test_bootstrap_idempotent(monkeypatch):
    # Patch environs.Env.read_env to track calls
    called = {}

    class DummyEnv:
        def read_env(self):
            called["env"] = True

    monkeypatch.setattr("research_agent_framework.bootstrap.Env", DummyEnv)

    # Patch rich.traceback.install
    monkeypatch.setattr("research_agent_framework.bootstrap._rich_traceback.install", lambda: called.setdefault("rich", True))

    # Patch loguru logger
    class DummyLogger:
        def remove(self):
            called["remove"] = True

        def add(self, sink, level, format):
            called["add"] = (sink, level, format)

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
    assert_that(called).contains("env")
    assert_that(called).contains("rich")
    assert_that(called).contains("remove")
    sink, level, fmt = called["add"]
    assert_that(callable(sink)).is_true()
    assert_that(level).is_equal_to("DEBUG")
    assert_that(fmt).is_equal_to("fmt")

    # Second call should do nothing
    called.clear()
    bs.bootstrap()
    assert_that(called).is_empty()

    # Force should re-run
    bs.bootstrap(force=True)
    assert_that(called).contains("env")
    assert_that(called).contains("rich")
    assert_that(called).contains("remove")
    sink, level, fmt = called["add"]
    assert_that(callable(sink)).is_true()
    assert_that(level).is_equal_to("DEBUG")
    assert_that(fmt).is_equal_to("fmt")


def test_bootstrap_env_read(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text("MODEL_NAME=from-env\n")

    # Create a minimal assertpy stub in the tmp_path so the subprocess can import it if needed
    assertpy_path = tmp_path / "assertpy.py"
    assertpy_path.write_text(
        textwrap.dedent(
            """
            def assert_that(x):
                class A:
                    def is_equal_to(self, y):
                        assert x == y

                    def is_true(self):
                        assert x

                    def is_instance_of(self, t):
                        assert isinstance(x, t)

                    def is_not_none(self):
                        assert x is not None

                    def contains(self, v):
                        assert v in x

                return A()
            """
        ),
        encoding="utf-8",
    )

    # Build a small, valid Python script for the subprocess to run
    src_path = os.path.abspath("src")
    script = textwrap.dedent(f"""
    import os
    import sys
    sys.path.insert(0, {src_path!r})
    # allow test to point to a specific .env
    os.environ["ENV_PATH"] = {str(env_path)!r}
    from research_agent_framework.bootstrap import bootstrap
    from research_agent_framework.config import get_settings

    bootstrap(force=True)
    print(get_settings(force_reload=True).model_name)
    """
    )

    result = __import__("subprocess").run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": src_path, "ENV_PATH": str(env_path)},
    )

    assert_that(result.returncode).is_equal_to(0)
    assert_that(result.stdout.strip()).is_equal_to("from-env")
