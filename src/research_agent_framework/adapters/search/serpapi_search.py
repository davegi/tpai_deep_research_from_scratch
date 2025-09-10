from typing import Dict, Union, List, Optional
import os
import json
import asyncio
import time

import httpx
from research_agent_framework.config import get_logger

from pydantic import TypeAdapter, HttpUrl

from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply, ReplyMeta
from research_agent_framework.models import SerpResult


class SerpAPISearchAdapter:
    """Minimal SerpAPI-like adapter stub used for testing `from_raw` behavior.

    This is a deterministic, in-process stub (no network calls). It demonstrates how a real adapter could implement `from_raw` to preserve
    raw payloads and normalize into `SerpResult` models.
    """

    def __init__(
        self,
        provider_name: str = "serpapi-stub",
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ) -> None:
        """If `api_key` is provided (or present in `SERPAPI_API_KEY`), the adapter will
        attempt a simple network call to `endpoint` when searching; otherwise it falls back to the deterministic in-process stub behavior
        used by tests.
        """
        self.provider_name = provider_name
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        # Allow overriding endpoint via env var or constructor; keep a safe default placeholder
        self.endpoint = endpoint or os.getenv("SERPAPI_ENDPOINT", "https://serpapi.example/search")

    @classmethod
    def from_raw(cls, raw: Dict[str, object]) -> "SerpAPISearchAdapter":
        provider = "serpapi"
        if isinstance(raw, dict) and raw.get("provider"):
            provider = str(raw.get("provider"))
        return cls(provider_name=provider)

    async def search(self, request: Union[str, SerpRequest]) -> SerpReply:
        # Accept legacy str queries for back-compat; normalize to SerpRequest
        if isinstance(request, str):
            request = SerpRequest(query=request, limit=10)

        # For the stub, respond with an empty reply when request.limit == 0
        if request.limit == 0:
            return SerpReply(results=[], meta=ReplyMeta(provider=self.provider_name, total_results=0))

        # If an API key is present and the endpoint is not a placeholder (contains "example"), attempt a network-backed search. Allow
        # forcing network via env var `SERPAPI_FORCE_NETWORK=1`.
        enable_network = (
            bool(self.api_key)
            and ("example" not in (self.endpoint or ""))
        ) or os.getenv("SERPAPI_FORCE_NETWORK") == "1"

        if enable_network:
            try:
                return await self._network_search(request)
            except Exception:
                # On any network failure, gracefully fall back to deterministic stub
                pass

        # Deterministic stub path (same as before)
        url_adapter = TypeAdapter(HttpUrl)
        url = url_adapter.validate_python("https://serpapi.example/item")

        raw_payload = {
            "title": f"Result for: {request.query}",
            "url": str(url),
            "snippet": "stub snippet",
            "provider": self.provider_name,
            "query": request.query,
        }
        r = SerpResult.from_raw(raw_payload, provider=self.provider_name)
        return SerpReply(results=[r], meta=ReplyMeta(provider=self.provider_name, total_results=1), raw={"inbound": True})

    async def _network_search(self, request: SerpRequest) -> SerpReply:
        """Perform a GET to the configured endpoint using httpx.AsyncClient with
        simple retries and timeouts. Expected JSON response with top-level `results`.
        """
        timeout = httpx.Timeout(10.0, read=10.0)
        max_retries = 3
        backoff_factor = 0.5

        async with httpx.AsyncClient(timeout=timeout) as client:
            params = {"q": request.query, "limit": request.limit, "api_key": self.api_key}
            last_exc: Optional[Exception] = None
            logger = get_logger()
            for attempt in range(1, max_retries + 1):
                try:
                    logger.debug(f"SerpAPI network search attempt {attempt} to {self.endpoint}")
                    resp = await client.get(self.endpoint, params=params, headers={"Accept": "application/json"})
                    resp.raise_for_status()
                    data = resp.json()
                    results = []
                    for item in data.get("results", []):
                        if isinstance(item, dict):
                            # Normalize provider-specific shapes
                            from research_agent_framework.adapters.search.mappers import map_serpapi_item

                            normalized = map_serpapi_item(item)
                            normalized.setdefault("provider", self.provider_name)
                            results.append(SerpResult.from_raw(normalized, provider=self.provider_name))
                    meta = ReplyMeta(provider=self.provider_name, total_results=len(results))
                    return SerpReply(results=results, meta=meta, raw=data if isinstance(data, dict) else {"response": data})
                except Exception as e:
                    logger.warning(f"SerpAPI network attempt {attempt} failed: {e}")
                    last_exc = e
                    if attempt < max_retries:
                        await asyncio.sleep(backoff_factor * (2 ** (attempt - 1)))
            # After retries
            logger.error(f"SerpAPI network search failed after {max_retries} attempts: {last_exc}")
            # Return an error reply instead of raising to allow callers to inspect meta
            meta = ReplyMeta(provider=self.provider_name, total_results=0, error=str(last_exc))
            return SerpReply(results=[], meta=meta, raw={"error": str(last_exc)})
