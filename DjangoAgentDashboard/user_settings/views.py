from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from .models import UserAPIKey
from .models import GitLabKey

class UserSettingsView(TemplateView):
    template_name = 'user_settings/user_settings.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["gitlab_key"] = GitLabKey.objects.filter(user=self.request.user).first()
        context["user_api_key"] = UserAPIKey.objects.filter(user=self.request.user).first()
        return context

class UpdateAPIKeyView(UpdateView):
    model = UserAPIKey
    fields = ['api_key']
    template_name = 'user_settings/user_apikey_form.html'
    success_url = '/settings/'

    def get_object(self, queryset=None):
        obj, created = UserAPIKey.objects.get_or_create(user=self.request.user)
        return obj

class UpdateGitLabKeyView(UpdateView):
    model = GitLabKey
    fields = ['gitlab_key']
    template_name = 'user_settings/user_gitlabkey_form.html'
    success_url = '/settings/'

    def get_object(self, queryset=None):
        obj, created = GitLabKey.objects.get_or_create(user=self.request.user)
        return obj
