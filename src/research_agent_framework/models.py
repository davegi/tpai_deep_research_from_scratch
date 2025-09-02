
from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated, Dict, List, Optional, Union

class Scope(BaseModel):
	topic: Annotated[str, Field(description="Main topic or subject of the research scope.", min_length=1)]
	description: Optional[str] = Field(default=None, description="Detailed description of the scope.")
	constraints: List[Annotated[str, Field(min_length=1)]] = Field(default_factory=list, description="List of constraints or boundaries for the research.")

class ResearchTask(BaseModel):
	id: Annotated[str, Field(description="Unique identifier for the research task.", min_length=1)]
	query: Annotated[str, Field(description="The research question or query to be addressed.", min_length=1)]
	context: Dict[str, Union[str, int, float, bool, None]] = Field(default_factory=dict, description="Additional context for the task, such as parameters or metadata.")
	notes: Optional[str] = Field(default=None, description="Optional notes or comments about the task.")

class EvalResult(BaseModel):
	task_id: Annotated[str, Field(description="ID of the evaluated research task.", min_length=1)]
	success: bool = Field(..., description="Whether the evaluation was successful.")
	score: float = Field(default=0.0, description="Numerical score for the evaluation.")
	feedback: Optional[str] = Field(default=None, description="Evaluator's feedback or comments.")
	details: Dict[str, Union[str, int, float, bool, None]] = Field(default_factory=dict, description="Additional details about the evaluation.")

class SerpResult(BaseModel):
	title: Annotated[str, Field(description="Title of the search result.", min_length=1)]
	url: Annotated[HttpUrl, Field(description="URL of the search result.")]
	snippet: Optional[str] = Field(default=None, description="Short snippet or summary from the search result.")
	raw: Dict[str, Union[str, int, float, bool, None]] = Field(default_factory=dict, description="Raw payload from the search provider.")
