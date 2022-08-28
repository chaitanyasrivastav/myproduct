from django.db import models
from django.contrib.auth.models import User
  
class Question(models.Model):
    title = models.CharField(max_length=150, unique=True)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title 