import os
import sys
from pathlib import Path

# Ensure the project's `src` directory is on sys.path for imports like `from research_agent_framework import ...`
ROOT = Path(__file__).parent.parent.resolve()
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
