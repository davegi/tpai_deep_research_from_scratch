
import pytest
from assertpy import assert_that
from research_agent_framework.prompts import renderer
from jinja2 import UndefinedError

# Test rendering with correct context
@pytest.mark.parametrize("template_name,context,expected_substr", [
    ("clarify_with_user_instructions.j2", {"messages": "msg", "date": "2025-09-05"}, "msg"),
    ("research_agent_prompt.j2", {"date": "2025-09-05"}, "research assistant conducting research"),
])
def test_render_template_success(template_name, context, expected_substr):
    result = renderer.render_template(template_name, context)
    assert_that(result, f"Rendered template '{template_name}' should contain expected substring '{expected_substr}'.").contains(expected_substr)

# Test StrictUndefined: missing variable raises
@pytest.mark.parametrize("template_name,context", [
    ("clarify_with_user_instructions.j2", {"date": "2025-09-05"}),  # missing 'messages'
    ("research_agent_prompt.j2", {}),  # missing 'date'
])
def test_render_template_missing_variable_raises(template_name, context):
    with pytest.raises(UndefinedError):
        renderer.render_template(template_name, context)
