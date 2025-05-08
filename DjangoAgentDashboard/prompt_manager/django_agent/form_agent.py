from agents import Agent
from .agent_models import FormsOutput

form_agent = Agent(
    name="FormAgent",
    instructions="""
You are a Django developer. For each model in a Django app, generate a corresponding `ModelForm` inside `forms.py`.

Include all fields using `fields = '__all__'`.

Output only the Python code.
""",
    output_type=FormsOutput
)
