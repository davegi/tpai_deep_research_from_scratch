import asyncio

from research_agent_framework.llm.client import MockLLM, LLMConfig


def test_mockllm_generate_is_deterministic():
    cfg = LLMConfig(api_key="", model="mock", temperature=0.0)
    client = MockLLM(cfg)

    async def run():
        r1 = await client.generate("Hello world")
        r2 = await client.generate("Hello world")
        return r1, r2

    r1, r2 = asyncio.run(run())
    assert r1 == r2
