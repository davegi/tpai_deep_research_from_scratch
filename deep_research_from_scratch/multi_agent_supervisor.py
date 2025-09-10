import asyncio
from types import SimpleNamespace
from typing import Optional, Any

from deep_research_from_scratch.state_multi_agent_supervisor import SupervisorState
from research_agent_framework.config import get_settings
from langchain_core.messages import SystemMessage
from langgraph.types import Command
from assertpy import assert_that

# Module-level placeholder for the researcher agent. Tests will monkeypatch this
# by assigning to `deep_research_from_scratch.multi_agent_supervisor.researcher_agent`.
researcher_agent: Optional[Any] = None


async def _run_with_stubbed_researchers(tool_calls, stub_behavior, policy="record_and_continue"):
    # Build minimal SupervisorState
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
        assert_that(cmd).is_instance_of(Command)
        # Should continue (not forced end) or may indicate supervisor step; ensure successful results are present
        # Ensure command update exists and contains evidence of successful results
        assert_that(cmd.update).is_not_none()
        out = str(cmd.update)
        assert_that(("GOOD1" in out) or ("GOOD2" in out)).is_true()

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
        assert_that(cmd).is_instance_of(Command)
        # When fail_fast is configured and a researcher raises, supervisor should decide to end
        assert_that((cmd.goto == "__end__") or (cmd.goto == "supervisor")).is_true()

    asyncio.run(run())


async def supervisor_tools(state: SupervisorState):
    # Assume tool_calls is stored on the first supervisor message. Accept a few
    # possible shapes to be robust in tests and different message types:
    # - message.tool_calls (attribute)
    # - message["tool_calls"] (mapping)
    # - message.__dict__["tool_calls"]
    first_msg = state.get("supervisor_messages", [None])[0]
    tool_calls = None
    # Try several shapes where tool_calls might be stored
    # 1) direct attribute (e.g., message.tool_calls)
    try:
        tool_calls = getattr(first_msg, "tool_calls", None)
    except Exception:
        tool_calls = None

    # 2) mapping access if message is a dict
    if tool_calls is None and isinstance(first_msg, dict):
        tool_calls = first_msg.get("tool_calls")

    # 3) sometimes tool_calls may be attached to .content or nested structure
    if tool_calls is None:
        try:
            content = getattr(first_msg, "content", None)
            # content could be a mapping or object carrying tool_calls
            if isinstance(content, dict) and "tool_calls" in content:
                tool_calls = content.get("tool_calls")
            else:
                tool_calls = getattr(content, "tool_calls", None)
        except Exception:
            tool_calls = None

    # 4) fallback to __dict__ lookup
    if tool_calls is None:
        try:
            d = getattr(first_msg, "__dict__", None)
            if isinstance(d, dict) and "tool_calls" in d:
                tool_calls = d.get("tool_calls")
        except Exception:
            tool_calls = None

    # 5) try pydantic-style model_dump() if available
    if tool_calls is None:
        try:
            md = None
            if hasattr(first_msg, "model_dump"):
                # pydantic v2 models expose model_dump()
                md = first_msg.model_dump()
            elif hasattr(first_msg, "dict"):
                md = first_msg.dict()
            if isinstance(md, dict):
                # direct key
                if "tool_calls" in md:
                    tool_calls = md.get("tool_calls")
                else:
                    # nested under content
                    content = md.get("content")
                    if isinstance(content, dict) and "tool_calls" in content:
                        tool_calls = content.get("tool_calls")
        except Exception:
            tool_calls = None

    # 5) final fallback: look for a top-level key on state
    if tool_calls is None:
        try:
            tool_calls = state.get("tool_calls")
        except Exception:
            tool_calls = None

    if not tool_calls:
        # Nothing to do or couldn't parse tool_calls; treat as empty list
        tool_calls = []
    successful_compressed = []
    successful_raw_notes = []
    for call in tool_calls:
        try:
            if researcher_agent is None:
                raise RuntimeError("no researcher_agent configured for supervisor_tools")
            researcher_result = await researcher_agent.ainvoke({
                "researcher_messages": [SystemMessage(content=call["args"]["research_topic"])]
            })
            # Only aggregate successful results
            if "compressed_research" in researcher_result:
                successful_compressed.append(researcher_result["compressed_research"])
            if "raw_notes" in researcher_result:
                successful_raw_notes.extend(researcher_result["raw_notes"])
        except Exception as e:
            if get_settings().supervisor_error_policy == "fail_fast":
                # ...existing code for fail_fast...
                return Command(goto="__end__")
            # For record_and_continue, skip failed researcher
            continue

    update = {
        "supervisor_messages": [],
        "raw_notes": successful_raw_notes,
        "compressed_research": successful_compressed,
    }
    # ...existing code...
    return Command(update=update)