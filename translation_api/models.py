from django.db import models
from django.contrib.auth.models import User

class Translation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_text = models.TextField()
    translated_text = models.TextField()
    content_type = models.CharField(max_length=20)  # 'html' or 'plain'
    target_language = models.CharField(max_length=50, default='English')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'