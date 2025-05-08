from django.db import models
from django.contrib.auth.models import User

class GitLabKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gitlab_key = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s GitLab Key"
    
class UserAPIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s API Key"