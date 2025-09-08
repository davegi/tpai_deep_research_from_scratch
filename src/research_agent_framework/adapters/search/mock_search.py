from typing import List, Union

from pydantic import TypeAdapter, HttpUrl

from research_agent_framework.models import SerpResult
from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply, ReplyMeta


class MockSearchAdapter:
    """Deterministic mock search adapter returning canned SerpResult items.

    Intended for unit and integration tests where network access is not allowed.
    Supports the new `SerpRequest`/`SerpReply` contract while keeping a
    backward-compatible `search(q: str)` shim.
    """

    async def search(self, request: Union[str, SerpRequest], **kwargs) -> Union[List[SerpResult], SerpReply]:
        # Accept either a raw query string (back-compat) or a SerpRequest.
        # For backwards compatibility, if called with a `str` return a list
        # of `SerpResult`. If called with `SerpRequest`, return a `SerpReply`.
        is_back_compat = isinstance(request, str)
        q = request if is_back_compat else request.query

        # Validate urls as HttpUrl to satisfy SerpResult type
        url_adapter = TypeAdapter(HttpUrl)
        url1 = url_adapter.validate_python("https://coffee.example.com/a")
        url2 = url_adapter.validate_python("https://coffee.example.com/b")

        r1 = SerpResult(
            title="Coffee Shop A",
            url=url1,
            snippet="Great coffee and friendly staff",
            raw={"q": q, "source": "mock", "id": 1},
        )
        r2 = SerpResult(
            title="Coffee Shop B",
            url=url2,
            snippet="Excellent pastries",
            raw={"q": q, "source": "mock", "id": 2},
        )

        if is_back_compat:
            return [r1, r2]
        reply = SerpReply(results=[r1, r2], meta=ReplyMeta(provider="mock", total_results=2))
        return reply

        @classmethod
        def from_raw(cls, raw: dict) -> 'MockSearchAdapter':
            """Factory to construct a MockSearchAdapter from a raw provider payload.

            For the mock adapter this simply returns an instance — the important
            contract is that adapters expose `from_raw` for consistency with real
            adapters which may need to normalize fields and preserve `raw`.
            """
            return cls()

