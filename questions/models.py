from django.db import models
from django.contrib.auth.models import User
  
class Question(models.Model):
    title = models.CharField(max_length=150, unique=True)
    content = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=150, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'questions'

    def __str__(self):
        return self.title