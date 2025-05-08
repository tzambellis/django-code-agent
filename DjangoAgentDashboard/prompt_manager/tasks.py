# ai_builder/tasks.py

from celery import shared_task
# from .django_agent import run_agents_chain  # wrap your async agents here
import asyncio
from .models import Prompt, PromptStatus
from prompt_manager.django_agent.main import main
from django.contrib.auth.models import User
from user_settings.models import GitLabKey, UserAPIKey
from agents import set_default_openai_key
import os
import subprocess
import shutil

def push_django_app_to_gitlab(repo_url_with_token, local_path, django_app_path, commit_message="Add Django app"):
    """
    repo_url_with_token: full GitLab repo URL including auth token
    local_path: temp path to clone into
    django_app_path: path to the Django app you want to push
    """
    if os.path.exists(local_path):
        shutil.rmtree(local_path)

    # Clone the repo
    subprocess.run(["git", "clone", repo_url_with_token, local_path], check=True)

    # Copy the Django app into the repo
    target_app_path = os.path.join(local_path, os.path.basename(django_app_path))
    shutil.copytree(django_app_path, target_app_path)

    # Git add/commit/push
    subprocess.run(["git", "add", "."], cwd=local_path, check=True)
    subprocess.run(["git", "commit", "-m", commit_message], cwd=local_path, check=True)
    subprocess.run(["git", "push"], cwd=local_path, check=True)

    print(f"✅ Django app pushed to: {repo_url_with_token}")


# tasks.py

import os
import shutil
import subprocess

from celery import shared_task
from user_settings.models import GitLabKey
from django.contrib.auth.models import User


# @shared_task
# def push_django_app_to_gitlab(gitlab_key, repo_path, app_path, commit_message="Scaffolded Django app"):
#     """
#     gitlab_key: Users Gitlab Key
#     repo_path: GitLab repo like 'username/repo-name'
#     app_path: absolute path to the Django app to push
#     """


#     repo_url = f"https://oauth2:{gitlab_key}@gitlab.com/{repo_path}.git"
#     local_repo_path = f"/tmp/gitlab_push_{app_path}"

#     if os.path.exists(local_repo_path):
#         shutil.rmtree(local_repo_path)

#     try:
#         # Clone
#         subprocess.run(["git", "clone", repo_url, local_repo_path], check=True)

#         # Copy app
#         target_path = os.path.join(local_repo_path, os.path.basename(app_path))
#         shutil.copytree(app_path, target_path)

#         # Commit and push
#         subprocess.run(["git", "add", "."], cwd=local_repo_path, check=True)
#         subprocess.run(["git", "commit", "-m", commit_message], cwd=local_repo_path, check=True)
#         subprocess.run(["git", "push"], cwd=local_repo_path, check=True)

#         return f"✅ Django app pushed to https://gitlab.com/{repo_path}"

#     except subprocess.CalledProcessError as e:
#         return f"❌ Git error: {e}"
#     except Exception as ex:
#         return f"❌ Failed: {ex}"
#     finally:
#         # Cleanup
#         if os.path.exists(local_repo_path):
#             shutil.rmtree(local_repo_path)

@shared_task
def run_agent_pipeline_task(user_id, prompt_id):
    prompt = Prompt.objects.get(id=prompt_id)

    prompt_text =prompt.text
    prompt_status, created = PromptStatus.objects.get_or_create(prompt=prompt)
    prompt_status.status = "pending"
    prompt_status.save()
    
    prompt_status.status = "processing"
    prompt_status.save()
    
    user = User.objects.get(id=user_id)
    # gitlab_key = GitLabKey.objects.get(user=user)
    api_key = UserAPIKey.objects.get(user=user).api_key

    set_default_openai_key(api_key)
    try:
        asyncio.run(main(prompt.text, prompt.id))
        prompt_status.status = "succeed"
        prompt_status.save()
    except Exception as e:
        prompt_status.status = "failed"
        prompt_status.save()
        raise e
