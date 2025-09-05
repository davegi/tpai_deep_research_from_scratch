

import pytest
from assertpy import assert_that
from research_agent_framework.prompts import renderer
from jinja2 import UndefinedError


import pytest
from assertpy import assert_that
from research_agent_framework.prompts import renderer
from jinja2 import UndefinedError
from hypothesis import given, strategies as st

TEMPLATE_NAMES = [
    "clarify_with_user_instructions.j2",
    "research_agent_prompt.j2"
]

class TestPromptRenderer:
    @pytest.mark.parametrize("template_name,context,expected_substr", [
        ("clarify_with_user_instructions.j2", {"messages": "msg", "date": "2025-09-05"}, "msg"),
        ("research_agent_prompt.j2", {"date": "2025-09-05"}, "research assistant conducting research"),
    ])
    def test_render_template_success(self, template_name, context, expected_substr):
        result = renderer.render_template(template_name, context)
        assert_that(result, f"Rendered template '{template_name}' should contain expected substring '{expected_substr}'.").contains(expected_substr)

    @pytest.mark.parametrize("template_name,context", [
        ("clarify_with_user_instructions.j2", {"date": "2025-09-05"}),  # missing 'messages'
        ("research_agent_prompt.j2", {}),  # missing 'date'
    ])
    def test_render_template_missing_variable_raises(self, template_name, context):
        with pytest.raises(UndefinedError):
            renderer.render_template(template_name, context)

    @pytest.mark.hypothesis
    @given(
        template_name=st.sampled_from(TEMPLATE_NAMES),
        messages=st.text(min_size=1, max_size=200),
        date=st.dates()
    )
    def test_clarify_with_user_instructions_valid(self, template_name, messages, date):
        if template_name == "clarify_with_user_instructions.j2":
            context = {"messages": messages, "date": str(date)}
            result = renderer.render_template(template_name, context)
            assert_that(result).contains(messages)
            assert_that(result).contains(str(date))

    @pytest.mark.hypothesis
    @given(
        template_name=st.just("clarify_with_user_instructions.j2"),
        context=st.dictionaries(st.text(min_size=1, max_size=10), st.text(), max_size=2)
    )
    def test_clarify_with_user_instructions_missing_keys(self, template_name, context):
        # Should raise if required keys are missing
        required = {"messages", "date"}
        if not required.issubset(context.keys()):
            with pytest.raises(UndefinedError):
                renderer.render_template(template_name, context)

    @pytest.mark.hypothesis
    @given(
        template_name=st.just("research_agent_prompt.j2"),
        date=st.dates()
    )
    def test_research_agent_prompt_valid(self, template_name, date):
        context = {"date": str(date)}
        result = renderer.render_template(template_name, context)
        assert_that(result).contains("research assistant conducting research")
        assert_that(result).contains(str(date))

    @pytest.mark.hypothesis
    @given(
        template_name=st.just("research_agent_prompt.j2"),
        context=st.dictionaries(st.text(min_size=1, max_size=10), st.text(), max_size=2)
    )
    def test_research_agent_prompt_missing_keys(self, template_name, context):
        # Should raise if required key 'date' is missing
        if "date" not in context:
            with pytest.raises(UndefinedError):
                renderer.render_template(template_name, context)
