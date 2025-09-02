import pytest
from pydantic import ValidationError, HttpUrl
from research_agent_framework.models import Scope, ResearchTask, EvalResult, SerpResult

def test_scope_happy_path():
    s = Scope(topic="AI", description="Artificial Intelligence", constraints=["no web search"])
    assert s.topic == "AI"
    assert s.description == "Artificial Intelligence"
    assert s.constraints == ["no web search"]

def test_scope_minimal():
    s = Scope(topic="AI")
    assert s.constraints == []
    assert s.description is None

def test_scope_invalid():
    with pytest.raises(ValidationError):
        Scope(topic="")
    # Remove None test: topic is required as str, None is not valid at type-check time

def test_research_task_happy_path():
    t = ResearchTask(id="t1", query="What is AI?", context={"foo": 1}, notes="note")
    assert t.id == "t1"
    assert t.query == "What is AI?"
    assert t.context["foo"] == 1
    assert t.notes == "note"

def test_research_task_minimal():
    t = ResearchTask(id="t1", query="Q?")
    assert t.context == {}
    assert t.notes is None

def test_research_task_invalid():
    with pytest.raises(ValidationError):
        ResearchTask(id="", query="Q?")
    with pytest.raises(ValidationError):
        ResearchTask(id="t1", query="")

def test_eval_result_happy_path():
    e = EvalResult(task_id="t1", success=True, score=0.9, feedback="ok", details={"foo": 2})
    assert e.task_id == "t1"
    assert e.success is True
    assert e.score == 0.9
    assert e.feedback == "ok"
    assert e.details["foo"] == 2

def test_eval_result_minimal():
    e = EvalResult(task_id="t1", success=False)
    assert e.score == 0.0
    assert e.feedback is None
    assert e.details == {}

def test_eval_result_invalid():
    with pytest.raises(ValidationError):
        EvalResult(task_id="", success=True)

def test_serp_result_happy_path():
    s = SerpResult(title="Result", url=HttpUrl('https://example.com'), snippet="summary", raw={"foo": 1})
    assert s.title == "Result"
    assert isinstance(s.url, HttpUrl)
    assert s.snippet == "summary"
    assert s.raw["foo"] == 1

def test_serp_result_minimal():
    s = SerpResult(title="Result", url=HttpUrl('https://example.com'))
    assert s.snippet is None
    assert s.raw == {}

def test_serp_result_invalid():
    with pytest.raises(ValidationError):
        SerpResult(title="", url=HttpUrl('https://example.com'))
    # The following test is for runtime validation, not static typing
    with pytest.raises(ValidationError):
        SerpResult.model_validate({"title": "Result", "url": "not-a-url"})
