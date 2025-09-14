import asyncio

from research_agent_framework.protocols import AgentContext
from research_agent_framework.mcp.stub import MCPStub
from research_agent_framework import evals


def test_agent_context_fields():
    ctx = AgentContext()
    # fields exist and default to None
    from assertpy import assert_that
    assert_that(hasattr(ctx, "settings"), description="AgentContext should have 'settings' attribute").is_true()
    assert_that(hasattr(ctx, "console"), description="AgentContext should have 'console' attribute").is_true()
    assert_that(hasattr(ctx, "logger"), description="AgentContext should have 'logger' attribute").is_true()
    assert_that(hasattr(ctx, "llm_client"), description="AgentContext should have 'llm_client' attribute").is_true()
    assert_that(hasattr(ctx, "search_adapter"), description="AgentContext should have 'search_adapter' attribute").is_true()


def test_evaluate_scores_length():
    # Short output yields low score, long output capped at 1.0
    short = evals.evaluate("t1", "short")
    long = evals.evaluate("t2", "x" * 500)
    from assertpy import assert_that
    assert_that(0.0 <= short.score < 1.0, description="Short output score should be in [0.0, 1.0)").is_true()
    assert_that(long.score, description="Long output score should be capped at 1.0").is_equal_to(1.0)


def test_mcp_stub_dispatch():
    bus = MCPStub()

    results = []

    async def handler(msg):
        results.append(msg)

    bus.register_handler("topic-a", handler)

    # run the publish in an event loop
    asyncio.run(bus.publish("topic-a", {"k": "v"}))

    from assertpy import assert_that
    assert_that(results, description="MCPStub should dispatch message correctly").is_equal_to([{"k": "v"}])
