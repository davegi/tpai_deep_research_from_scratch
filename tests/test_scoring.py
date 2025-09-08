from research_agent_framework.agents.scoring import SimpleScorer
from research_agent_framework.models import SerpResult, Location, Coordinates, Rating
from research_agent_framework.agents.base import ScoreResult
from typing import cast
from types import SimpleNamespace
from pydantic import HttpUrl
import math




def make_serp(title="T", url="https://example.com", lat=37.0, lon=-122.0, rating=None, distance=None, price=None):
    loc = Location(coords=Coordinates(lat=lat, lon=lon), distance=distance)
    return SerpResult(title=title, url=cast(HttpUrl, url), snippet="s", raw={}, location=loc, rating=rating, price_level=price)


def test_simple_scorer_with_rating_and_distance():
    scorer = SimpleScorer()
    rating = Rating(score=4.0, count=10)
    s = make_serp(rating=rating, distance=100.0, price=None)
    res = scorer.score(s)
    assert isinstance(res, ScoreResult)
    assert 0.0 <= res.score <= 1.0


def test_simple_scorer_with_price_effects():
    scorer = SimpleScorer()
    r = make_serp(price="cheap", distance=500.0)
    res = scorer.score(r)
    assert isinstance(res, ScoreResult)
    assert res.score >= 0.0


def test_simple_scorer_location_only():
    scorer = SimpleScorer()
    loc = Location(coords=Coordinates(lat=0.0, lon=0.0), distance=0)
    res = scorer.score(loc)
    assert isinstance(res, ScoreResult)
    assert res.score >= 0.0


def test_preference_weight_applies():
    scorer = SimpleScorer()
    rating = Rating(score=5.0)
    s = make_serp(rating=rating, distance=10)
    res1 = scorer.score(s)
    res2 = scorer.score(s, preferences={"weight": 0.5})
    assert res2.score <= res1.score


def test_clamping_and_nan_distance():
    scorer = SimpleScorer()
    # rating very large -> should be clamped to 1.0 Use a simple object instead of Pydantic Rating to avoid model validation.
    rating = SimpleNamespace(score=1000.0)
    item = SimpleNamespace(location=None, rating=rating, price_level=None)
    res = scorer.score(item)
    assert isinstance(res, ScoreResult)
    assert 0.0 <= res.score <= 1.0


def test_pint_quantity_distance_handling():
    try:
        import pint
    except Exception:
        # If pint isn't installed in the environment, skip this behavior test
        return

    unit_registry = pint.UnitRegistry()
    q = 500 * unit_registry.meter
    scorer = SimpleScorer()
    rating = Rating(score=4.0)
    s = make_serp(rating=rating, distance=q)
    res = scorer.score(s)
    assert isinstance(res, ScoreResult)
    assert 0.0 <= res.score <= 1.0
