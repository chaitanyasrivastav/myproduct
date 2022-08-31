from django.urls import path
from .views import (
    CreateAssessmentView, AssessmentDetailView,
    AssessmentQuestionCreateView
)

urlpatterns = [
    path('', CreateAssessmentView.as_view(), name='create_assessment'),
    path('<str:pk>', AssessmentDetailView.as_view(), name='assessment_detail'),
    path('<str:pk>/questions', AssessmentQuestionCreateView.as_view(), name='create_assessment_question'),
]