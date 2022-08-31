from django.db import models
from django.contrib.auth.models import User

from questions.models import Question
  
class Assessment(models.Model):
    title = models.CharField(max_length=150, unique=True)
    subject = models.CharField(max_length=150, null=True)
    tags = models.JSONField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class AssessmentUserJunction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)

class AssessmentQuestionJunction(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)


