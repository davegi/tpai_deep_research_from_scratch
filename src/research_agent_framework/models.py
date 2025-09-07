
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated, Dict, List, Optional, Union


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
	lat: float = Field(..., description="Latitude")
	lon: float = Field(..., description="Longitude")


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
	name: Optional[str] = Field(default=None)
	address: Optional[Address] = Field(default=None)
	coords: Optional[Coordinates] = Field(default=None)


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

