from django.contrib import admin
from .models import GitLabKey, UserAPIKey

@admin.register(GitLabKey)
class GitLabKeyAdmin(admin.ModelAdmin):
    list_display = ("user", "gitlab_key")
    search_fields = ("user__username", "gitlab_key")
    autocomplete_fields = ("user",)

@admin.register(UserAPIKey)
class UserAPIKeyAdmin(admin.ModelAdmin):
    list_display = ("user", "api_key")
    search_fields = ("user__username", "api_key")
    autocomplete_fields = ("user",)
