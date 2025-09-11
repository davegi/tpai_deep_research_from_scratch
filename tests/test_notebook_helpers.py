import asyncio

from research_agent_framework.protocols import AgentContext
from research_agent_framework.mcp.stub import MCPStub
from research_agent_framework import evals


def test_agent_context_fields():
    ctx = AgentContext()
    # fields exist and default to None
    assert hasattr(ctx, "settings")
    assert hasattr(ctx, "console")
    assert hasattr(ctx, "logger")
    assert hasattr(ctx, "llm_client")
    assert hasattr(ctx, "search_adapter")


def test_evaluate_scores_length():
    # Short output yields low score, long output capped at 1.0
    short = evals.evaluate("t1", "short")
    long = evals.evaluate("t2", "x" * 500)
    assert 0.0 <= short.score < 1.0
    assert long.score == 1.0


def test_mcp_stub_dispatch():
    bus = MCPStub()

    results = []

    async def handler(msg):
        results.append(msg)

    bus.register_handler("topic-a", handler)

    # run the publish in an event loop
    asyncio.run(bus.publish("topic-a", {"k": "v"}))

    assert results == [{"k": "v"}]
