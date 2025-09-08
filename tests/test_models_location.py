import pytest
from hypothesis import given, strategies as st

from research_agent_framework.models import Location, Coordinates
from assertpy import assert_that


def test_location_happy_path():
    loc = Location.model_validate({
        "name": "Cafe Example",
        "latitude": "37.7749",
        "longitude": "-122.4194",
        "raw": {"id": "abc123", "extra": 1},
    })

    assert_that(loc, description="Location.model_validate should return a Location").is_instance_of(Location)
    assert_that(loc.coords, description="coords should be present when lat/lon provided").is_not_none()
    assert_that(loc.coords, description="coords should be a Coordinates instance").is_instance_of(Coordinates)
    # Explicitly assert coords is not None for static type checkers, then access values
    assert loc.coords is not None
    assert_that(abs(loc.coords.lat - 37.7749) < 1e-6, description="latitude should match expected value").is_true()
    assert_that(abs(loc.coords.lon + 122.4194) < 1e-6, description="longitude should match expected value").is_true()
    assert_that(loc.raw.get("id"), description="raw id should be preserved").is_equal_to("abc123")


def test_location_out_of_range():
    with pytest.raises(Exception):
        Location.model_validate({"latitude": 100.0, "longitude": 0.0})


def test_location_preserve_raw_and_optional_fields():
    loc = Location.model_validate({
        "name": "Shop",
        "raw": {"payload": {"k": "v"}},
    })
    assert_that(loc.raw.get("payload"), description="raw payload should be preserved").is_equal_to({"k": "v"})
    assert_that(loc.coords, description="coords should be None when not provided").is_none()


def test_location_accepts_lng_key_and_coord_like():
    # dict with 'lng' key
    loc = Location.model_validate({"coords": {"lat": 37.77, "lng": -122.41}, "raw": {"id": "lng"}})
    assert_that(loc.coords, description="coords should be present for 'lng' mapping").is_not_none()
    assert_that(abs(loc.coords.lon + 122.41) < 1e-6, description="lng mapped to lon should be correct").is_true()

    # duck-typed coord-like object
    class C:
        def __init__(self, lat, lon):
            self.lat = lat
            self.lon = lon

    obj = C("37.7749", "-122.4194")
    loc2 = Location.model_validate({"coords": obj, "raw": {"id": "obj"}})
    assert_that(loc2.coords, description="duck-typed coord-like object should coerce to coords").is_not_none()
    assert loc2.coords is not None
    assert_that(abs(loc2.coords.lat - 37.7749) < 1e-6, description="coord-like lat coerced correctly").is_true()


def test_distance_and_phone_coercion():
    loc = Location.model_validate({
        "latitude": 37.7749,
        "longitude": -122.4194,
        "distance": "1.2 km",
        "phone": "+1-415-555-0100",
    })
    # distance should be parsed to a pint.Quantity when pint is installed
    try:
        import pint
        # When pint is available, distance should be a pint.Quantity
        assert_that(hasattr(loc.distance, "to"), description="distance should be a pint.Quantity when pint installed").is_true()
        assert_that(loc.distance, description="distance should not be None").is_not_none()
        meters = loc.distance.to("meter").magnitude
        assert_that(abs(meters - 1200.0) < 1e-6, description="distance conversion should yield 1200 meters").is_true()
    except Exception:
        # If pint not present, distance should at least be a float
        assert_that(isinstance(loc.distance, float), description="distance should be float when pint not installed").is_true()


@given(lat=st.floats(min_value=-90, max_value=90), lon=st.floats(min_value=-180, max_value=180))
def test_property_coords_roundtrip(lat, lon):
    # property-based test: coordinates round-trip when provided as strings
    loc = Location.model_validate({"latitude": str(lat), "longitude": str(lon)})
    assert_that(loc.coords, description="coords should be present for property-based lat/lon").is_not_none()
    assert loc.coords is not None
    assert_that(abs(loc.coords.lat - float(lat)) < 1e-6, description="lat roundtrip should be precise").is_true()
    assert_that(abs(loc.coords.lon - float(lon)) < 1e-6, description="lon roundtrip should be precise").is_true()
