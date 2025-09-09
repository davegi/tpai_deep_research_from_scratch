from __future__ import annotations

from typing import Dict, List

from pydantic import TypeAdapter, HttpUrl

from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply, ReplyMeta
from research_agent_framework.models import SerpResult


class SerpAPISearchAdapter:
    """Minimal SerpAPI-like adapter stub used for testing `from_raw` behavior.

    This is a deterministic, in-process stub (no network calls). It demonstrates
    how a real adapter could implement `from_raw` to preserve raw payloads and
    normalize into `SerpResult` models.
    """

    provider_name = "serpapi-stub"

    async def search(self, request: SerpRequest) -> SerpReply:
        # For the stub, respond with an empty reply when request.limit == 0
        if request.limit == 0:
            return SerpReply(results=[], meta=ReplyMeta(provider=self.provider_name, total_results=0))

        url_adapter = TypeAdapter(HttpUrl)
        url = url_adapter.validate_python("https://serpapi.example/item")

        r = SerpResult(title=f"Result for: {request.query}", url=url, snippet="stub snippet", raw={"raw_from": "serpapi", "query": request.query})
        return SerpReply(results=[r], meta=ReplyMeta(provider=self.provider_name, total_results=1), raw={"inbound": True})

    @classmethod
    def from_raw(cls, raw: Dict[str, object]) -> 'SerpAPISearchAdapter':
        # The factory could normalize API keys, endpoints etc. For this stub we
        # just return an instance; we preserve raw when constructing SerpResult
        # in search() above.
        return cls()
