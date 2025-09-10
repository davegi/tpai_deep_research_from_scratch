"""Evaluator utilities extracted from scoping notebook.

Provides a simple `evaluate` function that adapts an agent output to an
`EvalResult` and a small `Evaluator` class for extension.
"""
from typing import Any, Dict, Optional
from .models import EvalResult


def evaluate(task_id: str, output: str, details: Optional[Dict[str, Any]] = None) -> EvalResult:
    """Simple deterministic evaluator used by tests and demos.

    Produces an EvalResult with `score` derived heuristically from the
    output length and includes feedback as the raw output.
    """
    if details is None:
        details = {}
    score = min(1.0, max(0.0, len(output) / 100.0))
    return EvalResult(task_id=task_id, success=True, score=score, feedback=output, details=details)


class Evaluator:
    """Pluggable evaluator base class for tests to override."""

    def evaluate(self, task_id: str, output: str, details: Optional[Dict[str, Any]] = None) -> EvalResult:
        return evaluate(task_id, output, details)
