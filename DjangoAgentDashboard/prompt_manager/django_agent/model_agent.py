from agents import Agent, RunContextWrapper, function_tool

from .agent_models import ModelsOutput
# @function_tool
# async def fetch_project_structure(wrapper: RunContextWrapper[DjangoProjectPlan]) -> str:  
#     return wrapper.context


model_agent = Agent(
    name="ModelAgent",
    instructions="""
You are an expert Django developer. Based on the app name and a list of model names,
generate a valid Django `models.py` file. Include reasonable field definitions and
relations (like ForeignKey) if model names suggest relationships.

Output only the Python code.
""",
    # tools=[fetch_project_structure],
    output_type=ModelsOutput
)
