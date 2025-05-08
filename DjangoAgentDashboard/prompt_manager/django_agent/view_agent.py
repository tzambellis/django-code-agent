from agents import Agent

from .agent_models import ViewsOutput

view_agent = Agent(
    name="ViewAgent",
    instructions="""
You are a Django developer. For the given app and its list of views (like List, Detail, Create, Delete),
generate appropriate Django class-based views using generic views (e.g., ListView, DetailView, etc.).
Each view should be returned individually with its name and code.

Output only Python code for views.py.
""",
    output_type=ViewsOutput
)
