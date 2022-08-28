from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_question, name='create_question'),
    path('<str:username>', views.question_detail, name='question_detail'),
]