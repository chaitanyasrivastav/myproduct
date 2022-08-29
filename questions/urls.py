from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateQuestionView.as_view(), name='create_question'),
    path('<str:pk>', views.QuestionDetailView.as_view(), name='question_detail'),
]