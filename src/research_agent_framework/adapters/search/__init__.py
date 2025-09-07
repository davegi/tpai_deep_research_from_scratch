from typing import Protocol

from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply


class SearchAdapter(Protocol):
    async def search(self, request: SerpRequest) -> SerpReply: ...

    @classmethod
    def from_raw(cls, raw: dict) -> 'SearchAdapter': ...
