from typing import Dict

from pydantic import TypeAdapter, HttpUrl

from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply, ReplyMeta
from research_agent_framework.models import SerpResult


class TavilySearchAdapter:
    """Deterministic Tavily adapter stub for unit tests and demos.

    This adapter is a local, non-networking stub that implements `from_raw`
    and preserves inbound `raw` payloads into `SerpResult.raw`.
    """

    def __init__(self, provider_name: str = "tavily-stub") -> None:
        self.provider_name = provider_name

    @classmethod
    def from_raw(cls, raw: Dict[str, object]) -> "TavilySearchAdapter":
        provider = "tavily"
        if isinstance(raw, dict) and raw.get("provider"):
            provider = str(raw.get("provider"))
        return cls(provider_name=provider)

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
