from django.urls import path
from .views import (
    CreateQuestionView, QuestionDetailView
)

urlpatterns = [
    path('', CreateQuestionView.as_view(), name='create_question'),
    path('<str:pk>', QuestionDetailView.as_view(), name='question_detail'),
]