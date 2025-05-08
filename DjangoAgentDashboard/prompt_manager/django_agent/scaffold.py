# structure
import subprocess, os
from agents import Agent, function_tool
from .agent_models import FileWriteRequest

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
def create_django_project(project_name: str, destination_path: str) -> str:
    """
    destination_path: Path where the project will be created
    """
    # ensure_django_installed()
    print('creating project-----------------')
    destination_path = os.path.join("/tmp", destination_path)
    os.makedirs(destination_path, exist_ok=True)
    subprocess.run(["django-admin", "startproject", project_name], cwd=destination_path, check=True)
    return f"Created Django project: {project_name}"

@function_tool
def create_django_app(app_name: str, project_path: str) -> str:
    """
    destination_path: Path where the project will be created
    """
    print(project_path)
    print(app_name)
    try:
        subprocess.run(["python", "manage.py", "startapp", app_name], cwd=os.path.join("/tmp", project_path), check=True)
    except Exception as e:
        print(e)
    print('creating app-----------------')
    return f"Created Django app: {app_name}"

@function_tool
def write_file(request: FileWriteRequest) -> str:
    path = os.path.join("/tmp", request.path)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, request.filename)
    with open(file_path, "w") as f:
        f.write(request.content)
    return f"Wrote {file_path}"

scaffold_agent = Agent(
    name="ScaffoldAgent",
    instructions="You scaffold Django projects using the provided tools. Create the project, create the apps and add the new models, views, template, url, forms. create the model in the default model, views, urls in the default file created from the app create command",
    tools=[create_django_project, create_django_app, write_file]
)
