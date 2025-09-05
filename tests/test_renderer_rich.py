import pytest
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
    assert isinstance(output, str)
    assert len(output) > 0
    # For clarify template, check for JSON keys
    if template_name == "clarify_with_user_instructions.j2":
        assert 'need_clarification' in rendered
        assert 'question' in rendered
        assert 'verification' in rendered
    # For agent prompt, check for 'research assistant' phrase
    if template_name == "research_agent_prompt.j2":
        assert 'research assistant' in rendered
