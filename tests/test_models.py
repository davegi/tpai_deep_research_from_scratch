import pytest
from hypothesis import given, strategies as st
from pydantic import ValidationError, HttpUrl
from research_agent_framework.models import Scope, ResearchTask, EvalResult, SerpResult
from assertpy import assert_that

# -------------------- Scope Model Tests --------------------
class TestScope:
    def test_scope_serialization_deserialization(self):
        s = Scope(topic="AI", description="Artificial Intelligence", constraints=["no web search"])
        data = s.model_dump()
        s2 = Scope.model_validate(data)
        assert_that(s2).is_instance_of(Scope)
        assert_that(s2.topic).is_equal_to(s.topic)
        assert_that(s2.description).is_equal_to(s.description)
        assert_that(s2.constraints).is_equal_to(s.constraints)
    def test_scope_happy_path(self):
        s = Scope(topic="AI", description="Artificial Intelligence", constraints=["no web search"])
        assert_that(s.topic).is_equal_to("AI")
        assert_that(s.description).is_equal_to("Artificial Intelligence")
        assert_that(s.constraints).is_equal_to(["no web search"])

    def test_scope_minimal(self):
        s = Scope(topic="AI")
        assert_that(s.constraints).is_equal_to([])
        assert_that(s.description).is_none()

    def test_scope_invalid(self):
        with pytest.raises(ValidationError):
            Scope(topic="")

    # Property-based tests
    @pytest.mark.hypothesis
    @given(
        topic=st.text(min_size=1, max_size=100),
        description=st.one_of(st.none(), st.text(min_size=1, max_size=200)),
        constraints=st.lists(st.text(min_size=1, max_size=50), max_size=5)
    )
    def test_scope_property_valid(self, topic, description, constraints):
        s = Scope(topic=topic, description=description, constraints=constraints)
        assert_that(s.topic).is_equal_to(topic)
        assert_that(s.description).is_equal_to(description)
        assert_that(s.constraints).is_equal_to(constraints)

    @pytest.mark.hypothesis
    @given(
        topic=st.text(max_size=0)  # Empty string
    )
    def test_scope_property_invalid(self, topic):
        with pytest.raises(ValidationError):
            Scope(topic=topic)

# -------------------- ResearchTask Model Tests --------------------
class TestResearchTask:
    def test_research_task_serialization_deserialization(self):
        t = ResearchTask(id="t1", query="What is AI?", context={"foo": 1}, notes="note")
        data = t.model_dump()
        t2 = ResearchTask.model_validate(data)
        assert_that(t2).is_instance_of(ResearchTask)
        assert_that(t2.id).is_equal_to(t.id)
        assert_that(t2.query).is_equal_to(t.query)
        assert_that(t2.context).is_equal_to(t.context)
        assert_that(t2.notes).is_equal_to(t.notes)
    def test_research_task_happy_path(self):
        t = ResearchTask(id="t1", query="What is AI?", context={"foo": 1}, notes="note")
        assert_that(t.id).is_equal_to("t1")
        assert_that(t.query).is_equal_to("What is AI?")
        assert_that(t.context).contains("foo")
        assert_that(t.context["foo"]).is_equal_to(1)
        assert_that(t.notes).is_equal_to("note")

    def test_research_task_minimal(self):
        t = ResearchTask(id="t1", query="Q?")
        assert_that(t.context).is_equal_to({})
        assert_that(t.notes).is_none()

    def test_research_task_invalid(self):
        with pytest.raises(ValidationError):
            ResearchTask(id="", query="Q?")
        with pytest.raises(ValidationError):
            ResearchTask(id="t1", query="")

    # Property-based tests
    @pytest.mark.hypothesis
    @given(
        id=st.text(min_size=1, max_size=20),
        query=st.text(min_size=1, max_size=200),
        context=st.dictionaries(st.text(min_size=1, max_size=10), st.integers(), max_size=5),
        notes=st.one_of(st.none(), st.text(min_size=1, max_size=100))
    )
    def test_research_task_property_valid(self, id, query, context, notes):
        t = ResearchTask(id=id, query=query, context=context, notes=notes)
        assert_that(t.id).is_equal_to(id)
        assert_that(t.query).is_equal_to(query)
        assert_that(t.context).is_equal_to(context)
        assert_that(t.notes).is_equal_to(notes)

    @pytest.mark.hypothesis
    @given(
        id=st.text(max_size=0),
        query=st.text(min_size=1, max_size=200)
    )
    def test_research_task_property_invalid_id(self, id, query):
        with pytest.raises(ValidationError):
            ResearchTask(id=id, query=query)

    @pytest.mark.hypothesis
    @given(
        id=st.text(min_size=1, max_size=20),
        query=st.text(max_size=0)
    )
    def test_research_task_property_invalid_query(self, id, query):
        with pytest.raises(ValidationError):
            ResearchTask(id=id, query=query)

# -------------------- EvalResult Model Tests --------------------
class TestEvalResult:
    def test_eval_result_serialization_deserialization(self):
        e = EvalResult(task_id="t1", success=True, score=0.9, feedback="ok", details={"foo": 2})
        data = e.model_dump()
        e2 = EvalResult.model_validate(data)
        assert_that(e2).is_instance_of(EvalResult)
        assert_that(e2.task_id).is_equal_to(e.task_id)
        assert_that(e2.success).is_equal_to(e.success)
        assert_that(e2.score).is_close_to(e.score, 1e-6)
        assert_that(e2.feedback).is_equal_to(e.feedback)
        assert_that(e2.details).is_equal_to(e.details)
    def test_eval_result_happy_path(self):
        e = EvalResult(task_id="t1", success=True, score=0.9, feedback="ok", details={"foo": 2})
        assert_that(e.task_id).is_equal_to("t1")
        assert_that(e.success).is_true()
        assert_that(e.score).is_close_to(0.9, 1e-6)
        assert_that(e.feedback).is_equal_to("ok")
        assert_that(e.details).contains("foo")
        assert_that(e.details["foo"]).is_equal_to(2)

    def test_eval_result_minimal(self):
        e = EvalResult(task_id="t1", success=False)
        assert_that(e.score).is_close_to(0.0, 1e-6)
        assert_that(e.feedback).is_none()
        assert_that(e.details).is_equal_to({})

    def test_eval_result_invalid(self):
        with pytest.raises(ValidationError):
            EvalResult(task_id="", success=True)

    # Property-based tests
    @pytest.mark.hypothesis
    @given(
        task_id=st.text(min_size=1, max_size=20),
        success=st.booleans(),
        score=st.floats(min_value=0.0, max_value=1.0),
        feedback=st.one_of(st.none(), st.text(min_size=1, max_size=100)),
        details=st.dictionaries(st.text(min_size=1, max_size=10), st.integers(), max_size=5)
    )
    def test_eval_result_property_valid(self, task_id, success, score, feedback, details):
        e = EvalResult(task_id=task_id, success=success, score=score, feedback=feedback, details=details)
        assert_that(e.task_id).is_equal_to(task_id)
        assert_that(e.success).is_equal_to(success)
        assert_that(e.score).is_close_to(score, 1e-6)
        assert_that(e.feedback).is_equal_to(feedback)
        assert_that(e.details).is_equal_to(details)

    @pytest.mark.hypothesis
    @given(
        task_id=st.text(max_size=0),
        success=st.booleans()
    )
    def test_eval_result_property_invalid(self, task_id, success):
        with pytest.raises(ValidationError):
            EvalResult(task_id=task_id, success=success)

# -------------------- SerpResult Model Tests --------------------
class TestSerpResult:
    def test_serp_result_serialization_deserialization(self):
        s = SerpResult(title="Result", url=HttpUrl('https://example.com'), snippet="summary", raw={"foo": 1})
        data = s.model_dump()
        s2 = SerpResult.model_validate(data)
        assert_that(s2).is_instance_of(SerpResult)
        assert_that(s2.title).is_equal_to(s.title)
        assert_that(str(s2.url)).is_equal_to(str(s.url))
        assert_that(s2.snippet).is_equal_to(s.snippet)
        assert_that(s2.raw).is_equal_to(s.raw)
    def test_serp_result_happy_path(self):
        s = SerpResult(title="Result", url=HttpUrl('https://example.com'), snippet="summary", raw={"foo": 1})
        assert_that(s.title).is_equal_to("Result")
        assert_that(s.url).is_instance_of(HttpUrl)
        assert_that(s.snippet).is_equal_to("summary")
        assert_that(s.raw).contains("foo")
        assert_that(s.raw["foo"]).is_equal_to(1)

    def test_serp_result_minimal(self):
        s = SerpResult(title="Result", url=HttpUrl('https://example.com'))
        assert_that(s.snippet).is_none()
        assert_that(s.raw).is_equal_to({})

    def test_serp_result_invalid(self):
        with pytest.raises(ValidationError):
            SerpResult(title="", url=HttpUrl('https://example.com'))
        with pytest.raises(ValidationError):
            SerpResult.model_validate({"title": "Result", "url": "not-a-url"})

    # Property-based tests
    @pytest.mark.hypothesis
    @given(
        title=st.text(min_size=1, max_size=100),
        url=st.just('https://example.com'),
        snippet=st.one_of(st.none(), st.text(min_size=1, max_size=200)),
        raw=st.dictionaries(st.text(min_size=1, max_size=10), st.integers(), max_size=5)
    )
    def test_serp_result_property_valid(self, title, url, snippet, raw):
        validated_url = HttpUrl(url)
        s = SerpResult(title=title, url=validated_url, snippet=snippet, raw=raw)
        assert_that(s.title).is_equal_to(title)
        assert_that(s.url).is_instance_of(HttpUrl)
        assert_that(s.snippet).is_equal_to(snippet)
        assert_that(s.raw).is_equal_to(raw)

    @pytest.mark.hypothesis
    @given(
        title=st.text(max_size=0),
        url=st.just('https://example.com')
    )
    def test_serp_result_property_invalid(self, title, url):
        validated_url = HttpUrl(url)
        with pytest.raises(ValidationError):
            SerpResult(title=title, url=validated_url)
