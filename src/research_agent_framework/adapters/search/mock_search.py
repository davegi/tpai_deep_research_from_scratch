from typing import List

from pydantic import TypeAdapter, HttpUrl

from research_agent_framework.models import SerpResult


class MockSearchAdapter:
    """Deterministic mock search adapter returning canned SerpResult items.

    Intended for unit and integration tests where network access is not allowed.
    """

    async def search(self, q: str, **kwargs) -> List[SerpResult]:
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
        return [r1, r2]
