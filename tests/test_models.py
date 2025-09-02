import pytest
from pydantic import ValidationError, HttpUrl
from research_agent_framework.models import Scope, ResearchTask, EvalResult, SerpResult
from assertpy import assert_that

def test_scope_happy_path():
    s = Scope(topic="AI", description="Artificial Intelligence", constraints=["no web search"])
    assert_that(s.topic).is_equal_to("AI")
    assert_that(s.description).is_equal_to("Artificial Intelligence")
    assert_that(s.constraints).is_equal_to(["no web search"])

def test_scope_minimal():
    s = Scope(topic="AI")
    assert_that(s.constraints).is_equal_to([])
    assert_that(s.description).is_none()

def test_scope_invalid():
    with pytest.raises(ValidationError):
        Scope(topic="")
    # Remove None test: topic is required as str, None is not valid at type-check time

def test_research_task_happy_path():
    t = ResearchTask(id="t1", query="What is AI?", context={"foo": 1}, notes="note")
    assert_that(t.id).is_equal_to("t1")
    assert_that(t.query).is_equal_to("What is AI?")
    assert_that(t.context).contains("foo")
    assert_that(t.context["foo"]).is_equal_to(1)
    assert_that(t.notes).is_equal_to("note")

def test_research_task_minimal():
    t = ResearchTask(id="t1", query="Q?")
    assert_that(t.context).is_equal_to({})
    assert_that(t.notes).is_none()

def test_research_task_invalid():
    with pytest.raises(ValidationError):
        ResearchTask(id="", query="Q?")
    with pytest.raises(ValidationError):
        ResearchTask(id="t1", query="")

def test_eval_result_happy_path():
    e = EvalResult(task_id="t1", success=True, score=0.9, feedback="ok", details={"foo": 2})
    assert_that(e.task_id).is_equal_to("t1")
    assert_that(e.success).is_true()
    assert_that(e.score).is_close_to(0.9, 1e-6)
    assert_that(e.feedback).is_equal_to("ok")
    assert_that(e.details).contains("foo")
    assert_that(e.details["foo"]).is_equal_to(2)

def test_eval_result_minimal():
    e = EvalResult(task_id="t1", success=False)
    assert_that(e.score).is_close_to(0.0, 1e-6)
    assert_that(e.feedback).is_none()
    assert_that(e.details).is_equal_to({})

def test_eval_result_invalid():
    with pytest.raises(ValidationError):
        EvalResult(task_id="", success=True)

def test_serp_result_happy_path():
    s = SerpResult(title="Result", url=HttpUrl('https://example.com'), snippet="summary", raw={"foo": 1})
    assert_that(s.title).is_equal_to("Result")
    assert_that(s.url).is_instance_of(HttpUrl)
    assert_that(s.snippet).is_equal_to("summary")
    assert_that(s.raw).contains("foo")
    assert_that(s.raw["foo"]).is_equal_to(1)

def test_serp_result_minimal():
    s = SerpResult(title="Result", url=HttpUrl('https://example.com'))
    assert_that(s.snippet).is_none()
    assert_that(s.raw).is_equal_to({})

def test_serp_result_invalid():
    with pytest.raises(ValidationError):
        SerpResult(title="", url=HttpUrl('https://example.com'))
    # The following test is for runtime validation, not static typing
    with pytest.raises(ValidationError):
        SerpResult.model_validate({"title": "Result", "url": "not-a-url"})
