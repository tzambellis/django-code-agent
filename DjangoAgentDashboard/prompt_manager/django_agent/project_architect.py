from agents import Agent, Runner

from .agent_models import DjangoProjectPlan

project_architect = Agent(
  name="ProjectArchitectAgent",
  instructions="You are a senior Django software architect. Your job is to analyze the user's app idea and respond with a JSON plan to structure the Django project.",
  output_type=DjangoProjectPlan
)
