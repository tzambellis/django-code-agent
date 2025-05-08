from django.urls import path
from .views import CreatePromptView, UpdatePromptStatusView, PromptListView, PromptDeleteView, DownloadProjectZipView

urlpatterns = [
    path('create/', CreatePromptView.as_view(), name='create_prompt'),
    path('status/update/<int:pk>/', UpdatePromptStatusView.as_view(), name='update_prompt_status'),
    path('delete/<int:pk>/', PromptDeleteView.as_view(), name='delete_prompt'),
    path('', PromptListView.as_view(), name='prompt_list'),
    path('download/project/<int:project_id>/', DownloadProjectZipView.as_view(), name='download_project_zip'),
]