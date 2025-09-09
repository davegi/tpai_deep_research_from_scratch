from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Optional, Union, cast

from research_agent_framework.adapters.search.schema import SerpRequest, SerpReply
from research_agent_framework.models import SerpResult


class BaseSearchAdapter(ABC):
    provider_name: str = "base"

    @abstractmethod
    async def search(self, request: SerpRequest) -> SerpReply:
        raise NotImplementedError

    @classmethod
    def from_raw(cls, raw: Dict[str, object]) -> 'BaseSearchAdapter':
        # Default factory: not all adapters need to implement this, so raise
        raise NotImplementedError

    @staticmethod
    def preserve_raw_result(raw: Dict[str, object]) -> SerpResult:
        # Minimal mapping helper: preserve the raw dict and fill common fields
        from typing import cast, Optional
        from pydantic import TypeAdapter, HttpUrl

        title = cast(str, raw.get('title', '') or '')
        snippet = cast(Optional[str], raw.get('snippet'))

        url_val = raw.get('url', '') or ''
        # Validate/coerce url to HttpUrl; fall back to a known-safe URL if validation fails.
        try:
            url = TypeAdapter(HttpUrl).validate_python(url_val)
        except Exception:
            # fallback to a placeholder valid url to satisfy HttpUrl typing
            url = TypeAdapter(HttpUrl).validate_python('https://example.com')

        # Ensure raw is compatible type-wise (shallow conversion)
        safe_raw_any: Dict[str, object] = dict(raw)
        safe_raw = cast(Dict[str, Union[str, int, float, bool, None]], safe_raw_any)

        return SerpResult(
            title=title,
            url=url,
            snippet=snippet,
            raw=safe_raw,
        )
