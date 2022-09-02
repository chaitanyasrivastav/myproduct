from django.db import models
from django.contrib.auth.models import User
  
class Question(models.Model):
    title = models.CharField(max_length=150, unique=True)
    content = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=150, null=True)
    tags = models.JSONField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Choice(models.Model):
    content = models.CharField(max_length=250, null=True)
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    mark_as_answer = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
