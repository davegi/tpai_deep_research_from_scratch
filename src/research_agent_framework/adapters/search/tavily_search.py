from __future__ import annotations

from typing import Dict

from pydantic import TypeAdapter, HttpUrl

from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply, ReplyMeta
from research_agent_framework.models import SerpResult


class TavilySearchAdapter:
    """Deterministic Tavily adapter stub for unit tests and demos.

    This adapter is a local, non-networking stub that implements `from_raw`
    and preserves inbound `raw` payloads into `SerpResult.raw`.
    """

    provider_name = "tavily-stub"

    async def search(self, request: SerpRequest) -> SerpReply:
        # Empty limit -> empty reply
        if request.limit == 0:
            return SerpReply(results=[], meta=ReplyMeta(provider=self.provider_name, total_results=0))

        # Defensive URL creation using TypeAdapter(HttpUrl)
        url_adapter = TypeAdapter(HttpUrl)
        url = url_adapter.validate_python("https://tavily.example/item")

        r = SerpResult(
            title=f"Tavily result for: {request.query}",
            url=url,
            snippet="tavily stub snippet",
            raw={"provider": "tavily", "query": request.query},
        )

        return SerpReply(results=[r], meta=ReplyMeta(provider=self.provider_name, total_results=1))

    @classmethod
    def from_raw(cls, raw: Dict[str, object]) -> "TavilySearchAdapter":
        # In a real adapter this would extract API keys/endpoints. For the
        # stub we only expose the factory contract and allow tests to pass
        # arbitrary provider `raw` payloads through the SerpResult.raw field.
        return cls()
