import os
import sys
import warnings
from pathlib import Path

# Silence noisy deprecation warnings coming from third-party packages (Pydantic v2 migration warnings)
# These warnings originate from dependency code (for example langchain internals referencing `__fields__`).
# We filter by substring to avoid depending on the exact warning class path.
warnings.filterwarnings("ignore", message=r".*__fields__.*")

# Ensure the project's `src` directory is on sys.path for imports like `from research_agent_framework import ...`
ROOT = Path(__file__).parent.parent.resolve()
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
