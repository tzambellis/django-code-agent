from django.contrib import admin
from .models import Prompt, PromptStatus

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("text_short", "created_at")
    search_fields = ("text",)
    ordering = ("-created_at",)

    def text_short(self, obj):
        return obj.text[:50]
    text_short.short_description = "Prompt Text"

@admin.register(PromptStatus)
class PromptStatusAdmin(admin.ModelAdmin):
    list_display = ("prompt_summary", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("prompt__text",)

    def prompt_summary(self, obj):
        return obj.prompt.text[:50]
    prompt_summary.short_description = "Prompt"