from typing import Optional, Protocol, Union, List

from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply

# Import known adapters so we can expose a simple factory that dispatches by
# provider name. Adapters implement `from_raw(raw: dict) -> Adapter` where
# applicable.
from research_agent_framework.adapters.search.mock_search import MockSearchAdapter
from research_agent_framework.adapters.search.serpapi_search import SerpAPISearchAdapter
from research_agent_framework.adapters.search.tavily_search import TavilySearchAdapter
from research_agent_framework.models import SerpResult


class SearchAdapter(Protocol):
    # Support both legacy `str` queries and the canonical `SerpRequest` and
    # allow either a legacy list-of-results or a `SerpReply` structured reply.
    async def search(self, request: Union[str, SerpRequest]) -> Union[List[SerpResult], SerpReply]: ...

    @classmethod
    def from_raw(cls, raw: dict) -> 'SearchAdapter': ...


def from_raw_adapter(raw: dict, provider: Optional[str] = None) -> SearchAdapter:
    """Dispatch to a provider-specific adapter factory to preserve raw payloads.

    This helper provides a single place callers can use to obtain a SearchAdapter
    from a provider raw payload. For unknown providers default to the Mock
    adapter which preserves the payload but is safe for tests.
    """
    prov = (provider or raw.get("provider") or raw.get("source") or "mock").lower()
    if prov == "mock":
        return MockSearchAdapter.from_raw(raw)
    if prov in ("serpapi", "google"):
        return SerpAPISearchAdapter.from_raw(raw)
    if prov == "tavily":
        return TavilySearchAdapter.from_raw(raw)
    # Fallback: return a mock adapter that preserves raw
    return MockSearchAdapter.from_raw(raw)
