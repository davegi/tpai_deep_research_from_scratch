from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from research_agent_framework.models import SerpResult, Location


class SerpRequest(BaseModel):
    """Core, provider-agnostic search request contract."""

    query: str = Field(..., min_length=1, description="User query text")
    limit: int = Field(default=10, ge=0, description="Maximum number of results requested")
    location: Optional[Location] = Field(default=None, description="Optional location context")
    provider_params: Dict[str, object] = Field(default_factory=dict, description="Provider-specific parameters preserved as raw")


class ReplyMeta(BaseModel):
    provider: Optional[str] = Field(default=None)
    total_results: Optional[int] = Field(default=None)
    elapsed_ms: Optional[int] = Field(default=None)
    error: Optional[str] = Field(default=None)


class SerpReply(BaseModel):
    results: List[SerpResult] = Field(default_factory=list)
    meta: ReplyMeta = Field(default_factory=ReplyMeta)
    raw: Dict[str, object] = Field(default_factory=dict, description="Original provider payload preserved at leaf")
