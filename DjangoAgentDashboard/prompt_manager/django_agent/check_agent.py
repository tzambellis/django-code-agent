# structure
import subprocess, os
from agents import Agent, function_tool, gen_trace_id, trace, Runner
from .agent_models import FileWriteRequest
from agents.mcp import MCPServer, MCPServerStdio

import os
import platform

def get_venv_python_bin():
    if platform.system() == "Windows":
        path = os.path.join(".venv", "Scripts", "python.exe")
    else:
        path = os.path.join(".venv", "bin", "python")
    return os.path.abspath(path)

def get_venv_pip_bin():
    if platform.system() == "Windows":
        path = os.path.join(".venv", "Scripts", "pip.exe")
    else:
        path = os.path.join(".venv", "bin", "pip")
    return os.path.abspath(path)


def ensure_django_installed():
    subprocess.run(["python3", "-m", "venv", ".venv"], check=True)
    subprocess.run([get_venv_pip_bin(), "install", "django"], check=True)

@function_tool
def create_django_project(project_name: str) -> str:
    ensure_django_installed()
    subprocess.run(["django-admin", "startproject", project_name], check=True)
    print('creating Project----------')
    return f"Created Django project: {project_name}"

@function_tool
def create_django_app(app_name: str, project_path: str) -> str:
    subprocess.run([get_venv_python_bin(), "manage.py", "startapp", app_name], cwd=project_path, check=True)
    print('creating app-----------------')
    return f"Created Django app: {app_name}"

@function_tool
def write_file(request: FileWriteRequest) -> str:
    os.makedirs(request.path, exist_ok=True)
    file_path = os.path.join(request.path, request.filename)
    with open(file_path, "w") as f:
        f.write(request.content)
    return f"Wrote {file_path}"


async def run(server, input, context):
    scaffold_agent = Agent(
        name="ScaffoldAgent",
        instructions="You scaffold Django projects using the provided tools. Create the project, create the apps and add the new models, views, template, url, forms, update the settings.py so it has the new apps in the installed apps and the crispy forms",
        mcp_servers=[server],
        tools=[create_django_project]
    )
    result = await Runner.run(
        starting_agent=scaffold_agent,
        input=input,
        context=context,
    )
    print(result.final_output)


async def run_scaffold_agent(input, context):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", current_dir],
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="MCP Filesystem Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server, input, context)