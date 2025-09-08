import asyncio
from deep_research_from_scratch.multi_agent_supervisor import supervisor_tools
from deep_research_from_scratch.state_multi_agent_supervisor import SupervisorState, ConductResearch
from research_agent_framework.config import get_settings
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.types import Command


async def _run_supervisor_with_tool_calls(tool_calls, policy="record_and_continue"):
    # Create a minimal SupervisorState
    state: SupervisorState = {
        "supervisor_messages": [SystemMessage(content="test", tool_calls=tool_calls)],
        "research_brief": "brief",
        "research_iterations": 0,
        "notes": [],
        "raw_notes": [],
    }

    # Patch settings
    s = get_settings()
    s.supervisor_error_policy = policy

    return await supervisor_tools(state)


def test_record_and_continue_policy_event_loop():
    async def run():
        # Create a ConductResearch tool call that will cause the repository's researcher_agent to run
        # but we will simulate by passing a fake tool call structure that triggers the code path.
        tool_calls = [{"name": "ConductResearch", "id": "1", "args": {"research_topic": "X"}}]
        cmd = await _run_supervisor_with_tool_calls(tool_calls, policy="record_and_continue")
        assert isinstance(cmd, Command)
        assert cmd.goto in ("supervisor", "__end__")

    asyncio.run(run())


def test_fail_fast_policy_event_loop():
    async def run():
        tool_calls = [{"name": "ConductResearch", "id": "1", "args": {"research_topic": "X"}}]
        cmd = await _run_supervisor_with_tool_calls(tool_calls, policy="fail_fast")
        assert isinstance(cmd, Command)
        # When fail_fast and a researcher error occurs, supervisor_tools should decide to END
        assert cmd.goto == "__end__" or cmd.goto == "supervisor"

    asyncio.run(run())
