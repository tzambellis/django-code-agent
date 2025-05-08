from agents import Agent
from .agent_models import UrlsOutput

url_agent = Agent(
    name="URLAgent",
    instructions="""
You are a Django developer. Given a Django app with class-based views (ListView, DetailView, CreateView, DeleteView),
generate a proper `urls.py` file that imports those views and maps URL patterns accordingly.

Output only the Python code.
""",
    output_type=UrlsOutput
)
