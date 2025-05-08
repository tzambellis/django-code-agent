from agents import Agent

from .agent_models import TemplatesOutput

template_agent = Agent(
    name="TemplateAgent",
    instructions="""
You are a Django frontend developer. For each view in a Django app (List, Detail, Create, Delete),
generate a basic Tailwind-compatible HTML template.

Each output should include the view name and the HTML content.

Only return valid HTML code.
""",
    output_type=TemplatesOutput
)
