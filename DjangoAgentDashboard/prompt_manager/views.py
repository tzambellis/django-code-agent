from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.db.models import Prefetch
from .models import Prompt
from .models import PromptStatus
from .tasks import run_agent_pipeline_task 
from user_settings.models import UserAPIKey
from user_settings.models import GitLabKey
from django.contrib import messages
from django.shortcuts import redirect


import os
import zipfile
import io
from django.http import HttpResponse, Http404
from django.views import View

class CreatePromptView(CreateView):
    model = Prompt
    fields = ['text']
    template_name = 'prompt_manager/prompt_form.html'
    success_url = '/prompts/'
    
    def form_valid(self, form):
        # form.instance.created_at = timezone.now()
        user = self.request.user
        # gitlab_key = GitLabKey.objects.filter(user=user).first()
        api_key = UserAPIKey.objects.filter(user=user).first()

        if not api_key:
            messages.error(self.request, "You must set both your API key before creating a prompt.")
            return redirect("user_settings")  # or use `reverse()` if needed

        form.instance.user = user
        response = super().form_valid(form)
        run_agent_pipeline_task.delay(self.request.user.id, form.instance.id)
        return response

class UpdatePromptStatusView(UpdateView):
    model = PromptStatus
    fields = ['status']
    template_name = 'prompt_manager/promptstatus_form.html'
    success_url = '/prompts/status/'

class PromptListView(ListView):
    model = Prompt
    template_name = 'prompt_manager/prompt_list.html'
    context_object_name = 'prompts'

    def get_queryset(self):
        return Prompt.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                'promptstatus_set',
                queryset=PromptStatus.objects.all(),
                to_attr='status_list'
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["gitlab_key"] = GitLabKey.objects.filter(user=self.request.user).first()
        context["user_api_key"] = UserAPIKey.objects.filter(user=self.request.user).first()
        return context

class PromptDeleteView(DeleteView):
    model = Prompt
    template_name = 'prompt_manager/prompt_confirm_delete.html'
    success_url = reverse_lazy('prompt_list')


class DownloadProjectZipView(View):
    def get(self, request, project_id):
        folder_path = f"/tmp/project_{project_id}"

        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            raise Http404("Projektordner nicht gefunden.")

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zip_file.write(file_path, arcname)

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="project_{project_id}.zip"'
        return response