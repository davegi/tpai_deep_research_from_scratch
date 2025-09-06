import pytest
import asyncio
from hypothesis import given, strategies as st

from research_agent_framework.agents.base import ResearchAgent
from research_agent_framework.models import Scope, ResearchTask
from research_agent_framework.llm.client import MockLLM, LLMConfig
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter


def test_plan_single_task_no_constraints():
    scope = Scope(topic='Coffee Shops', description='Find the best in SF')
    agent = ResearchAgent(llm_client=None)
    tasks = agent.plan(scope)
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    assert isinstance(tasks[0], ResearchTask)


def test_plan_with_constraints():
    scope = Scope(topic='Coffee', constraints=['no paid', 'open now'])
    agent = ResearchAgent(llm_client=None)
    tasks = agent.plan(scope)
    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_run_uses_mockllm():
    cfg = LLMConfig(api_key='x', model='m')
    mock = MockLLM(cfg)
    agent = ResearchAgent(llm_client=mock)
    task = ResearchTask(id='t1', query='best coffee in soma')
    res = await agent.run(task)
    assert res.task_id == task.id
    assert res.success is True
    assert res.feedback is not None
    assert 'mock response for' in res.feedback


@given(prompt=st.text(min_size=1, max_size=100))
def test_property_based_plan_and_run(prompt):
    # Property-based: construct a scope from random prompt and assert plan/run types
    scope = Scope(topic=prompt)
    agent = ResearchAgent(llm_client=MockLLM(LLMConfig(api_key='x', model='m')))
    tasks = agent.plan(scope)
    assert tasks
    # pick first task and run via asyncio loop
    task = tasks[0]
    res = asyncio.get_event_loop().run_until_complete(agent.run(task))
    assert res.task_id == task.id
    assert isinstance(res.score, float)
