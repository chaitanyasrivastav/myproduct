from django.urls import path
from .views import (
    CreateQuestionView, QuestionDetailView,
    CreateAnswerView, AnswerDetailView,
    CreateChoiceView, ChoiceDetailView
)

urlpatterns = [
    path('', CreateQuestionView.as_view(), name='create_question'),
    path('<str:pk>', QuestionDetailView.as_view(), name='question_detail'),
    path('<str:question_id>/answer', CreateAnswerView.as_view(), name='create_answer'),
    path('<str:question_id>/answer/<str:pk>', AnswerDetailView.as_view(), name='answer_detail'),
    path('<str:question_id>/choice', CreateChoiceView.as_view(), name='create_choice'),
    path('<str:question_id>/choice/<str:pk>', ChoiceDetailView.as_view(), name='choice_detail'),
]