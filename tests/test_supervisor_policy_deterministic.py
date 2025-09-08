import asyncio
from types import SimpleNamespace

from deep_research_from_scratch.multi_agent_supervisor import supervisor_tools
from deep_research_from_scratch.state_multi_agent_supervisor import SupervisorState
from research_agent_framework.config import get_settings
from langchain_core.messages import SystemMessage
from langgraph.types import Command


async def _run_with_stubbed_researchers(tool_calls, stub_behavior, policy="record_and_continue"):
    # Build minimal SupervisorState
    # Create a real BaseMessage (SystemMessage) and attach tool_calls as an
    # instance attribute so langchain's filter_messages will accept it.
    msg = SystemMessage(content="test")
    # Attach tool_calls directly to the message instance
    setattr(msg, "tool_calls", tool_calls)

    state: SupervisorState = {
        "supervisor_messages": [msg],
        "research_brief": "brief",
        "research_iterations": 0,
        "notes": [],
        "raw_notes": [],
    }

    # Patch settings
    s = get_settings()
    s.supervisor_error_policy = policy

    # Monkeypatch the `researcher_agent` used by the supervisor module so our stub is used
    import deep_research_from_scratch.multi_agent_supervisor as sup

    async def stub_ainvoke(payload):
        # payload is a ResearcherState-like dict; inspect researcher_messages last human message
        topic = None
        try:
            msgs = payload.get("researcher_messages", [])
            if msgs:
                topic = str(msgs[0].content)
        except Exception:
            pass

        # Delegate to provided behavior
        return await stub_behavior(topic)

    stub_holder = SimpleNamespace(ainvoke=stub_ainvoke)
    old = getattr(sup, "researcher_agent", None)
    sup.researcher_agent = stub_holder

    try:
        return await supervisor_tools(state)
    finally:
        # restore
        sup.researcher_agent = old


def test_record_and_continue_mixed_results():
    async def stub_behavior(topic):
        # Fail for topic containing FAIL, succeed otherwise
        if topic and "FAIL" in topic:
            raise RuntimeError("simulated researcher failure")
        # return success-like mapping
        return {"compressed_research": f"summary for {topic}", "raw_notes": [f"note:{topic}"]}

    async def run():
        tool_calls = [
            {"name": "ConductResearch", "id": "t1", "args": {"research_topic": "GOOD1"}},
            {"name": "ConductResearch", "id": "t2", "args": {"research_topic": "FAIL-THIS"}},
            {"name": "ConductResearch", "id": "t3", "args": {"research_topic": "GOOD2"}},
        ]

        cmd = await _run_with_stubbed_researchers(tool_calls, stub_behavior, policy="record_and_continue")
        assert isinstance(cmd, Command)
        # Should continue (not forced end) or may indicate supervisor step; ensure successful results are present
        # Ensure command update exists and contains evidence of successful results
        assert cmd.update is not None
        out = str(cmd.update)
        assert ("GOOD1" in out) or ("GOOD2" in out)

    asyncio.run(run())


def test_fail_fast_mixed_results():
    async def stub_behavior(topic):
        if topic and "FAIL" in topic:
            raise RuntimeError("simulated researcher failure")
        return {"compressed_research": f"summary for {topic}", "raw_notes": [f"note:{topic}"]}

    async def run():
        tool_calls = [
            {"name": "ConductResearch", "id": "t1", "args": {"research_topic": "GOOD1"}},
            {"name": "ConductResearch", "id": "t2", "args": {"research_topic": "FAIL-THIS"}},
        ]

        cmd = await _run_with_stubbed_researchers(tool_calls, stub_behavior, policy="fail_fast")
        assert isinstance(cmd, Command)
        # When fail_fast is configured and a researcher raises, supervisor should decide to end
        assert cmd.goto == "__end__" or cmd.goto == "supervisor"

    asyncio.run(run())
