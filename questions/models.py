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

class Answer(models.Model):
    content = models.CharField(max_length=250)
    description = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{"+f'"{str(self.id)}": "{self.content}"'+"}"

class Choice(models.Model):
    content = models.CharField(max_length=250, null=True)
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    mark_as_answer = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{"+f'"{str(self.id)}": "{self.content}"'+"}"
