from typing import Protocol, runtime_checkable, List, Dict, Any, Optional, TypedDict
from uuid import uuid4

from research_agent_framework.models import Scope, ResearchTask, EvalResult


@runtime_checkable
class Agent(Protocol):
	def plan(self, scope: Scope) -> List[ResearchTask]:
		raise NotImplementedError()

	async def run(self, task: ResearchTask) -> EvalResult:
		raise NotImplementedError()


class ResearchAgent:
	"""Minimal ResearchAgent implementation used for tests and notebooks.

	This agent is intentionally small: it converts a `Scope` into one or more
	`ResearchTask` instances via `plan`, and executes a single task via `run` by
	delegating to an injected async LLM client. The implementation is deterministic
	and lightweight so unit tests and property-based tests can exercise behavior.
	"""

	def __init__(self, llm_client, search_adapter: Optional[Any] = None):
		# llm_client: any object with `async def generate(prompt: str) -> str`
		self.llm = llm_client
		self.search = search_adapter

	def plan(self, scope: Scope) -> List[ResearchTask]:
		"""Create a small list of ResearchTask from the provided Scope.

		Current simple heuristic:
		- One task per constraint (if present), otherwise a single task using the
		  scope.topic and scope.description.
		"""
		tasks: List[ResearchTask] = []
		if scope.constraints:
			for i, c in enumerate(scope.constraints, start=1):
				q = f"{scope.topic} - constraint: {c}"
				tasks.append(ResearchTask(id=str(uuid4())[:8], query=q, context={"constraint": c}))
		else:
			q = scope.topic
			if scope.description:
				q = f"{q}: {scope.description}"
			tasks.append(ResearchTask(id=str(uuid4())[:8], query=q, context={}))
		return tasks

	async def run(self, task: ResearchTask) -> EvalResult:
		"""Execute a ResearchTask by generating text from the LLM client and
		returning a simple EvalResult derived from the response.

		This is intentionally deterministic for testing: score is derived from
		the response length (clipped to [0,1]) and feedback includes the raw LLM
		output.
		"""
		# Prefer model-in / model-out when available on the LLM client.
		if hasattr(self.llm, "generate_model"):
			try:
				res = await self.llm.generate_model(task, EvalResult)
				# ensure returned value is EvalResult
				if isinstance(res, EvalResult):
					return res
			except Exception:
				# fall back to text-based API below
				pass

		# Fallback: use text-based generation and wrap into EvalResult
		prompt = task.query
		output = await self.llm.generate(prompt)
		score = min(1.0, max(0.0, len(output) / 100.0))
		return EvalResult(task_id=task.id, success=True, score=score, feedback=output, details={"prompt": prompt})


# ------------------------- Scoring protocol -------------------------
class ScoreResult(TypedDict):
	score: float
	reason: str
	meta: Dict[str, Any]


@runtime_checkable
class ScoringProtocol(Protocol):
	"""Protocol for scoring items (SerpResult or Location).

	Implementations should return a ScoreResult mapping with a normalized
	`score` in [0.0, 1.0].
	"""

	def score(self, item: Any, preferences: Optional[Dict[str, Any]] = None) -> ScoreResult:
		raise NotImplementedError()
