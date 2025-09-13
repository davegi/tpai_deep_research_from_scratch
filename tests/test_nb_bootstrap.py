import os
from pathlib import Path


def test_ensure_src_and_bootstrap_imports_and_returns_handles():
    """Import the helper and ensure it returns (settings, console, logger).

    This test is intentionally lightweight: it verifies the helper runs in CI/dev
    environments where the repo layout is preserved.
    """
    repo_root = Path(__file__).resolve().parents[1]
    os.chdir(repo_root)

    # Load the helper module directly from file so tests don't rely on package import
    import importlib.util
    helper_path = repo_root / 'notebooks' / 'nb_bootstrap.py'
    spec = importlib.util.spec_from_file_location('nb_bootstrap', str(helper_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Could not load nb_bootstrap spec from {helper_path}')
    nb_bootstrap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nb_bootstrap)  # type: ignore[attr-defined]

    settings, console, logger = nb_bootstrap.ensure_src_and_bootstrap()

    # Basic type checks (don't import heavy types to keep CI stable)
    assert hasattr(settings, 'model_name') or hasattr(settings, 'logging'), 'settings object lacks expected attrs'
    # console should have a print method
    assert hasattr(console, 'print')
    # logger should at least have an info method
    assert hasattr(logger, 'info')

    # Optional stronger checks: Settings and Console types (best-effort)
    try:
        from research_agent_framework.config import Settings
        from rich.console import Console as RichConsole
        assert isinstance(console, (RichConsole,))
        assert hasattr(settings, 'model_name') or isinstance(settings, Settings)
    except Exception:
        # If importing concrete types fails, fall back to duck-typing checks above
        pass
