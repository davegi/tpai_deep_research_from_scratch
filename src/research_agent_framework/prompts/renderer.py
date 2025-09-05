from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    undefined=StrictUndefined,
    autoescape=False,
)

def render_template(template_name: str, context: dict) -> str:
    """
    Renders a Jinja2 template with StrictUndefined. Raises an error if any variable is missing in context.
    """
    template = _env.get_template(template_name)
    return template.render(context)
