from django.urls import path
from .views import UserSettingsView, UpdateAPIKeyView, UpdateGitLabKeyView

urlpatterns = [
    path('', UserSettingsView.as_view(), name='user_settings'),
    path('api-key/', UpdateAPIKeyView.as_view(), name='update_api_key'),
    path('gitlab-key/', UpdateGitLabKeyView.as_view(), name='update_gitlab_key'),
]