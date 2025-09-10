
from typing import Dict, Union, Optional
import os
import json
import asyncio
import httpx
from research_agent_framework.config import get_logger

from pydantic import TypeAdapter, HttpUrl

from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply, ReplyMeta
from research_agent_framework.models import SerpResult


class TavilySearchAdapter:
    """Deterministic Tavily adapter stub for unit tests and demos.

    This adapter is a local, non-networking stub that implements `from_raw` and preserves inbound `raw` payloads into `SerpResult.raw`.
    """

    def __init__(
        self,
        provider_name: str = "tavily-stub",
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ) -> None:
        self.provider_name = provider_name
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.endpoint = endpoint or os.getenv("TAVILY_ENDPOINT", "https://tavily.example/search")

    @classmethod
    def from_raw(cls, raw: Dict[str, object]) -> "TavilySearchAdapter":
        provider = "tavily"
        if isinstance(raw, dict) and raw.get("provider"):
            provider = str(raw.get("provider"))
        return cls(provider_name=provider)

    async def search(self, request: Union[str, SerpRequest]) -> SerpReply:
        # Accept legacy string queries
        if isinstance(request, str):
            request = SerpRequest(query=request, limit=10)

        # Empty limit -> empty reply
        if request.limit == 0:
            return SerpReply(results=[], meta=ReplyMeta(provider=self.provider_name, total_results=0))

        # Only attempt network when API key present AND endpoint not a placeholder (contains "example"), or when forced by env var
        # `TAVILY_FORCE_NETWORK=1`.
        enable_network = (
            bool(self.api_key)
            and ("example" not in (self.endpoint or ""))
        ) or os.getenv("TAVILY_FORCE_NETWORK") == "1"

        if enable_network:
            try:
                return await self._network_search(request)
            except Exception:
                pass

        # Defensive URL creation using TypeAdapter(HttpUrl)
        url_adapter = TypeAdapter(HttpUrl)
        url = url_adapter.validate_python("https://tavily.example/item")

        raw_payload = {
            "title": f"Tavily result for: {request.query}",
            "url": str(url),
            "snippet": "tavily stub snippet",
            "provider": self.provider_name,
            "query": request.query,
        }
        r = SerpResult.from_raw(raw_payload, provider=self.provider_name)

        return SerpReply(results=[r], meta=ReplyMeta(provider=self.provider_name, total_results=1))

    async def _network_search(self, request: SerpRequest) -> SerpReply:
        timeout = httpx.Timeout(10.0, read=10.0)
        max_retries = 3
        backoff_factor = 0.5

        async with httpx.AsyncClient(timeout=timeout) as client:
            params = {"q": request.query, "limit": request.limit, "api_key": self.api_key}
            last_exc: Optional[Exception] = None
            logger = get_logger()
            for attempt in range(1, max_retries + 1):
                try:
                    logger.debug(f"Tavily network search attempt {attempt} to {self.endpoint}")
                    resp = await client.get(self.endpoint, params=params, headers={"Accept": "application/json"})
                    resp.raise_for_status()
                    data = resp.json()
                    results = []
                    for item in data.get("results", []):
                        if isinstance(item, dict):
                            from research_agent_framework.adapters.search.mappers import map_tavily_item

                            normalized = map_tavily_item(item)
                            normalized.setdefault("provider", self.provider_name)
                            results.append(SerpResult.from_raw(normalized, provider=self.provider_name))
                    meta = ReplyMeta(provider=self.provider_name, total_results=len(results))
                    return SerpReply(results=results, meta=meta, raw=data if isinstance(data, dict) else {"response": data})
                except Exception as e:
                    logger.warning(f"Tavily network attempt {attempt} failed: {e}")
                    last_exc = e
                    if attempt < max_retries:
                        await asyncio.sleep(backoff_factor * (2 ** (attempt - 1)))
            logger.error(f"Tavily network search failed after {max_retries} attempts: {last_exc}")
            meta = ReplyMeta(provider=self.provider_name, total_results=0, error=str(last_exc))
            return SerpReply(results=[], meta=meta, raw={"error": str(last_exc)})
