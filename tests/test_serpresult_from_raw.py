import pytest

from research_agent_framework.models import SerpResult
from pydantic import ValidationError


def test_serpresult_from_raw_happy_path():
    raw = {"title": "Cafe X", "url": "https://example.com/cafex", "snippet": "Nice coffee", "provider": "mock", "id": 42}
    r = SerpResult.from_raw(raw)
    assert isinstance(r, SerpResult)
    assert r.title == "Cafe X"
    assert str(r.url) == "https://example.com/cafex"
    assert r.raw["id"] == 42
    assert r.provider_meta is not None and r.provider_meta.provider == "mock"


def test_serpresult_from_raw_missing_url_raises():
    raw = {"title": "Cafe NoURL", "description": "No url provided"}
    with pytest.raises(ValueError):
        SerpResult.from_raw(raw)
