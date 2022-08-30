from django.urls import path
from .views import (
    CreateAnswerView, AnswerDetailView
)

urlpatterns = [
    path('', CreateAnswerView.as_view(), name='create_answer'),
    path('<str:pk>', AnswerDetailView.as_view(), name='answer_detail'),
]