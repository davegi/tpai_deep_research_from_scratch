"""
Encapsulates repo src path detection and sys.path setup for notebooks and scripts.
"""
import sys
from pathlib import Path

def ensure_src_in_syspath():
    """Detects the repo src directory and adds it to sys.path if needed."""
    repo_cwd = Path.cwd().resolve()
    found_src = None
    for candidate in [repo_cwd] + list(repo_cwd.parents):
        if (candidate / "src" / "research_agent_framework").exists():
            found_src = (candidate / "src").resolve()
            break
    if found_src is None:
        candidate = (repo_cwd / ".." / "src").resolve()
        if (candidate / "research_agent_framework").exists():
            found_src = candidate
    if found_src is not None and str(found_src) not in sys.path:
        sys.path.insert(0, str(found_src))
    return found_src
