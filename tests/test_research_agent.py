def test_scope_state_capture_and_validation():
    """
    Mirrors notebook: validates scope state object after clarification.
    """
    from deep_research_from_scratch.research_agent_scope import scope_research, AgentInputState
    from langchain_core.messages import HumanMessage
    from assertpy import assert_that

    from typing import Sequence
    from langchain_core.messages import AnyMessage
    from typing import cast
    user_messages = [
        HumanMessage(content="Find the best coffee shops in SF."),
        HumanMessage(content="I want places open now and not paid."),
        HumanMessage(content="No cover charge, open now, highest ratings in SOMA.")
    ]
    input_state = AgentInputState(messages=cast(list[AnyMessage], user_messages))
    from research_agent_framework.config import get_console
    from rich.markdown import Markdown
    console = get_console()
    result = scope_research.invoke(input_state)
    assert_that(result).contains_key("research_brief")
    assert_that(result["research_brief"]).is_not_empty()
    console.print(Markdown(f"**Research brief:**\n\n{result['research_brief']}"))
import pytest
import asyncio
from hypothesis import given, strategies as st
from assertpy import assert_that

from research_agent_framework.agents.base import ResearchAgent
from research_agent_framework.models import Scope, ResearchTask
from research_agent_framework.llm.client import MockLLM, LLMConfig
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter


def test_plan_single_task_no_constraints():
    scope = Scope(topic='Coffee Shops', description='Find the best in SF')
    agent = ResearchAgent(llm_client=None)
    tasks = agent.plan(scope)
    assert_that(tasks, description="plan() should return a list of ResearchTask").is_instance_of(list)
    assert_that(len(tasks), description="plan() should produce exactly 1 task when no constraints").is_equal_to(1)
    assert_that(tasks[0], description="first planned item should be a ResearchTask").is_instance_of(ResearchTask)


def test_plan_with_constraints():
    scope = Scope(topic='Coffee', constraints=['no paid', 'open now'])
    agent = ResearchAgent(llm_client=None)
    tasks = agent.plan(scope)
    assert_that(len(tasks), description="plan() should produce one task per constraint").is_equal_to(2)


@pytest.mark.asyncio
async def test_run_uses_mockllm():
    cfg = LLMConfig(api_key='x', model='m')
    mock = MockLLM(cfg)
    agent = ResearchAgent(llm_client=mock)
    task = ResearchTask(id='t1', query='best coffee in soma')
    res = await agent.run(task)
    assert_that(res.task_id, description="EvalResult.task_id should match the task id").is_equal_to(task.id)
    assert_that(res.success, description="EvalResult.success should be True for MockLLM").is_true()
    assert_that(res.feedback, description="EvalResult.feedback should be populated").is_not_none()
    assert_that(res.feedback, description="MockLLM feedback should contain marker").contains('mock response for')


@given(prompt=st.text(min_size=1, max_size=100))
def test_property_based_plan_and_run(prompt):
    # Property-based: construct a scope from random prompt and assert plan/run types
    scope = Scope(topic=prompt)
    agent = ResearchAgent(llm_client=MockLLM(LLMConfig(api_key='x', model='m')))
    tasks = agent.plan(scope)
    assert_that(tasks, description="plan() should produce at least one task").is_not_empty()
    # pick first task and run via asyncio loop
    task = tasks[0]
    res = asyncio.run(agent.run(task))
    assert_that(res.task_id, description="model-out run: task_id should be preserved").is_equal_to(task.id)
    assert_that(res.score, description="EvalResult.score should be a float").is_instance_of(float)
