
from enum import Enum
from typing import Annotated, Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field, HttpUrl, field_validator

# Assume pydantic-extra-types and pint are available in the environment
import pydantic_extra_types as pet
import pint
_pint_unit_registry = pint.UnitRegistry()


# ------------------------- Core models -------------------------
class Scope(BaseModel):
	topic: Annotated[str, Field(description="Main topic or subject of the research scope.", min_length=1)]
	description: Optional[str] = Field(default=None, description="Detailed description of the scope.")
	constraints: List[Annotated[str, Field(min_length=1)]] = Field(
		default_factory=list, description="List of constraints or boundaries for the research."
	)


class ResearchTask(BaseModel):
	id: Annotated[str, Field(description="Unique identifier for the research task.", min_length=1)]
	query: Annotated[str, Field(description="The research question or query to be addressed.", min_length=1)]
	context: Dict[str, Union[str, int, float, bool, None]] = Field(
		default_factory=dict,
		description="Additional context for the task, such as parameters or metadata.",
	)
	notes: Optional[str] = Field(default=None, description="Optional notes or comments about the task.")


class EvalResult(BaseModel):
	task_id: Annotated[str, Field(description="ID of the evaluated research task.", min_length=1)]
	success: bool = Field(..., description="Whether the evaluation was successful.")
	score: float = Field(default=0.0, description="Numerical score for the evaluation.")
	feedback: Optional[str] = Field(default=None, description="Evaluator's feedback or comments.")
	details: Dict[str, Union[str, int, float, bool, None]] = Field(
		default_factory=dict, description="Additional details about the evaluation."
	)


# ------------------------- SerpAPI-style nested models -------------------------
class PriceLevel(str, Enum):
	FREE = "free"
	CHEAP = "cheap"
	MODERATE = "moderate"
	EXPENSIVE = "expensive"


class Coordinates(BaseModel):
	"""Simple latitude/longitude container used when a lightweight typed object is preferred.

	This class remains the default internal representation but will accept stringy numeric values
	and coerce them to floats where possible.
	"""
	lat: float = Field(..., description="Latitude")
	lon: float = Field(..., description="Longitude")

	@field_validator("lat", "lon", mode="before")
	def _coerce_numeric(cls, v: Any) -> Any:
		if v is None:
			return v
		# Accept numeric strings
		if isinstance(v, str):
			v = v.strip()
			if v == "":
				raise ValueError("empty string is not a valid coordinate")
			try:
				return float(v)
			except Exception:
				raise ValueError(f"cannot parse coordinate value: {v!r}")
		return v

	@field_validator("lat")
	def _lat_range(cls, v: float) -> float:
		if v < -90 or v > 90:
			raise ValueError("latitude must be between -90 and 90")
		return v

	@field_validator("lon")
	def _lon_range(cls, v: float) -> float:
		if v < -180 or v > 180:
			raise ValueError("longitude must be between -180 and 180")
		return v


class Address(BaseModel):
	street: Optional[str] = Field(default=None)
	city: Optional[str] = Field(default=None)
	region: Optional[str] = Field(default=None)
	postal_code: Optional[str] = Field(default=None)
	country: Optional[str] = Field(default=None)


class Rating(BaseModel):
	score: Optional[float] = Field(default=None, ge=0.0, le=5.0)
	count: Optional[int] = Field(default=None, ge=0)


class Location(BaseModel):
	"""Unified Location model used across adapters and agents.

	This model prefers structured `coords: Coordinates` but also accepts separate `latitude` / `longitude`
	inputs. When available, it will accept objects from `pydantic-extra-types` (e.g. `Coordinate`) and
	will normalize unit-bearing values using `pint` when present.
	"""

	name: Optional[str] = Field(default=None, description="Human-readable name of the place")
	address: Optional[Address] = Field(default=None)
	coords: Optional[Coordinates] = Field(default=None, description="Structured coords (preferred)")
	latitude: Optional[float] = Field(default=None, description="Latitude (optional, deprecated in favor of coords)")
	longitude: Optional[float] = Field(default=None, description="Longitude (optional, deprecated in favor of coords)")
	phone: Optional[str] = Field(default=None, description="Contact phone number; normalized to E.164 when possible")
	url: Optional[HttpUrl] = Field(default=None)
	source: Optional[str] = Field(default=None, description="Provider/source of this location record")
	distance: Optional[Any] = Field(default=None, description="Optional distance (may be a pint.Quantity when pint is available)")
	raw: Dict[str, Any] = Field(default_factory=dict, description="Raw payload from the upstream adapter/provider")

	@field_validator("coords", mode="before")
	def _accept_pet_coordinate(cls, v: Any) -> Any:
		# Accept pydantic-extra-types Coordinate objects or simple mappings
		if v is None:
			return v
		# Accept objects that expose `lat` and `lon` attributes (duck-typed pydantic-extra-types or similar)
		if hasattr(v, "lat") and hasattr(v, "lon"):
			lat = getattr(v, "lat", None)
			lon = getattr(v, "lon", None)
			return {"lat": lat, "lon": lon}
		# accept mapping with lat/lon
		if isinstance(v, dict) and "lat" in v and ("lon" in v or "lng" in v):
			lon_key = "lon" if "lon" in v else "lng"
			return {"lat": v.get("lat"), "lon": v.get(lon_key)}
		return v

	@field_validator("latitude", "longitude", mode="before")
	def _coerce_lat_lon(cls, v: Any) -> Any:
		# Accept numeric strings and coerce to float
		if v is None:
			return v
		if isinstance(v, str):
			v = v.strip()
			if v == "":
				return None
			try:
				return float(v)
			except Exception:
				raise ValueError("latitude/longitude must be numeric or empty")
		return v

	@field_validator("phone", mode="before")
	def _normalize_phone(cls, v: Any) -> Any:
		if v is None:
			return v
		# Accept phone-like objects (duck-typed) and coerce to string
		if not isinstance(v, str):
			try:
				return str(v)
			except Exception:
				pass
		# otherwise, coerce to str and return
		return str(v)

	@field_validator("distance", mode="before")
	def _normalize_distance(cls, v: Any) -> Any:
		if v is None:
			return v
		# If pint is available, prefer returning a pint.Quantity
		if _pint_unit_registry is not None:
			if isinstance(v, str):
				try:
					return _pint_unit_registry(v)
				except Exception:
					# fall back to numeric parse
					pass
			if isinstance(v, (int, float)):
				return _pint_unit_registry(str(v) + " meter")
			# If already a pint.Quantity, return as-is
			if isinstance(v, pint.Quantity):
				return v
		# Without pint, accept numeric values only
		if isinstance(v, (int, float)):
			return float(v)
		# try to parse numeric strings
		if isinstance(v, str):
			v2 = v.strip()
			try:
				return float(v2)
			except Exception:
				raise ValueError("distance could not be parsed; install pint for unit support")
		raise ValueError("unsupported distance type")

	@field_validator("coords", mode="after")
	def _build_coords_from_lat_lon(cls, v: Any, info: Any) -> Any:
		# If coords were provided as dict (from earlier coercion), build Coordinates
		if isinstance(v, dict) and "lat" in v and "lon" in v:
			return Coordinates(lat=v["lat"], lon=v["lon"])
		return v

	@field_validator("coords", "latitude", "longitude", mode="after")
	def _ensure_coords_consistency(cls, v: Any, info: Any) -> Any:
		# This validator is intentionally simple; cross-field composition happens in model_validator.
		return v

	@classmethod
	def model_validate(cls, data: Any) -> "Location":
		# Use pydantic's default model_validate but add cross-field logic: if latitude/longitude provided
		# and coords is missing, construct coords.
		if isinstance(data, dict) and ("latitude" in data or "longitude" in data):
			lat = data.get("latitude")
			lon = data.get("longitude")
			if lat is not None and lon is not None and data.get("coords") is None:
				data = dict(data)
				data["coords"] = {"lat": lat, "lon": lon}
		return super().model_validate(data)


class ProviderMeta(BaseModel):
	provider: Optional[str] = Field(default=None)
	id: Optional[Union[str, int]] = Field(default=None)
	raw: Dict[str, Union[str, int, float, bool, None]] = Field(default_factory=dict)


class SerpResult(BaseModel):
	"""Search engine / provider result.  

	Backwards-compatible fields (`title`, `url`, `snippet`, `raw`) are kept.
	For SerpAPI-style responses, nested models are available (optional) to
	encourage decomposition of complex payloads into typed models.
	"""

	# Backwards-compatible simple fields used in many tests/demo code
	title: Annotated[str, Field(description="Title of the search result.", min_length=1)]
	url: Annotated[HttpUrl, Field(description="URL of the search result.")]
	snippet: Optional[str] = Field(default=None, description="Short snippet or summary from the search result.")
	raw: Dict[str, Union[str, int, float, bool, None]] = Field(default_factory=dict, description="Raw payload from the search provider.")

	# Nested, decomposed fields (optional)
	location: Optional[Location] = Field(default=None, description="Structured location information, if available.")
	rating: Optional[Rating] = Field(default=None, description="Structured rating information, if available.")
	price_level: Optional[PriceLevel] = Field(default=None, description="Optional price level enum.")
	categories: List[str] = Field(default_factory=list, description="List of category strings")
	provider_meta: Optional[ProviderMeta] = Field(default=None, description="Provider-specific metadata and raw id/payload")

	@classmethod
	def from_raw(cls, raw: dict, provider: Optional[str] = None) -> "SerpResult":
		"""Construct a SerpResult from a provider raw payload.

		This factory attempts to normalize common provider payload keys into the
		simple `title`, `url`, `snippet` shape while preserving the original
		payload under `raw` and attaching provider metadata under `provider_meta`.

		It is intentionally permissive: missing optional fields are left as
		None, but `title` and `url` are required by the model and therefore
		callers should provide payloads that contain at least those fields or
		handle `ValidationError` raised by pydantic.
		"""
		title = None
		url = None
		snippet = None

		if not isinstance(raw, dict):
			raise TypeError("raw payload must be a dict")

		# Common provider keys -> normalize
		# title/name
		if "title" in raw and raw.get("title"):
			title = raw.get("title")
		elif "name" in raw and raw.get("name"):
			title = raw.get("name")

		# url/link
		if "url" in raw and raw.get("url"):
			url = raw.get("url")
		elif "link" in raw and raw.get("link"):
			url = raw.get("link")

		# snippet/description
		if "snippet" in raw and raw.get("snippet"):
			snippet = raw.get("snippet")
		elif "description" in raw and raw.get("description"):
			snippet = raw.get("description")

		provider_meta = ProviderMeta(provider=provider or raw.get("provider"), id=raw.get("id"), raw=raw)

		# Construct using pydantic validation (HttpUrl and required fields enforced)
		# Do not coerce missing url to empty string; require a present URL
		url_value = url or raw.get("url") or raw.get("link")
		if not url_value:
			raise ValueError("cannot build SerpResult.from_raw without a URL in raw payload")
		return cls(title=title or "", url=url_value, snippet=snippet, raw=raw, provider_meta=provider_meta)

