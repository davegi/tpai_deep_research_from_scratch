import pytest

from research_agent_framework.models import SerpResult
from pydantic import ValidationError
from assertpy import assert_that


def test_serpresult_from_raw_happy_path():
    raw = {"title": "Cafe X", "url": "https://example.com/cafex", "snippet": "Nice coffee", "provider": "mock", "id": 42}
    r = SerpResult.from_raw(raw)
    assert_that(r).is_instance_of(SerpResult)
    assert_that(r.title).is_equal_to("Cafe X")
    assert_that(str(r.url)).is_equal_to("https://example.com/cafex")
    assert_that(r.raw["id"]).is_equal_to(42)
    # Guard and split provider_meta checks to avoid attribute access on None
    assert_that(r.provider_meta).is_not_none()
    if r.provider_meta is not None:
        assert_that(r.provider_meta.provider).is_equal_to("mock")


def test_serp_result_from_raw_missing_url_raises():
    raw = {"title": "Cafe NoURL", "description": "No url provided"}
    with pytest.raises(ValueError):
        SerpResult.from_raw(raw)
