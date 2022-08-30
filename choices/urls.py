from django.urls import path
from .views import (
    CreateChoiceView, ChoiceDetailView
)

urlpatterns = [
    path('', CreateChoiceView.as_view(), name='create_choice'),
    path('<str:pk>', ChoiceDetailView.as_view(), name='choice_detail'),
]