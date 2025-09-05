
import pytest
from assertpy import assert_that
from research_agent_framework.prompts import renderer
from rich.markdown import Markdown
from rich.console import Console
from io import StringIO

@pytest.mark.parametrize("template_name,context", [
    ("clarify_with_user_instructions.j2", {"messages": "User: What are the best coffee shops in SF?", "date": "2025-09-05"}),
    ("research_agent_prompt.j2", {"date": "2025-09-05"}),
])
def test_render_template_rich_markdown(template_name, context):
    # Render template
    rendered = renderer.render_template(template_name, context)
    # Render markdown using rich
    md = Markdown(rendered)
    buf = StringIO()
    console = Console(file=buf, force_terminal=True, color_system=None)
    console.print(md)
    output = buf.getvalue()
    # Save output to file (overwrite if exists)
    out_path = f"tests/test_renderer_rich_output_{template_name.replace('.j2','')}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    # Check that some expected content is present in the rich output
    assert_that(output, "Rich output should be a string.").is_instance_of(str)
    assert_that(len(output), "Rich output should not be empty.").is_greater_than(0)
    # For clarify template, check for JSON keys
    if template_name == "clarify_with_user_instructions.j2":
        assert_that(rendered, "Rendered clarify template should contain 'need_clarification'.").contains('need_clarification')
        assert_that(rendered, "Rendered clarify template should contain 'question'.").contains('question')
        assert_that(rendered, "Rendered clarify template should contain 'verification'.").contains('verification')
    # For agent prompt, check for 'research assistant' phrase
    if template_name == "research_agent_prompt.j2":
        assert_that(rendered, "Rendered agent prompt should contain 'research assistant'.").contains('research assistant')
