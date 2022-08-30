from django.db import models
from questions.models import Question
from django.contrib.auth.models import User

# Create your models here.
class Answer(models.Model):
    content = models.CharField(max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'questions'

    def __str__(self):
        return self.content
