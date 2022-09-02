from django.urls import path
from .views import (
    CreateAssessmentView, AssessmentDetailView,
    AssessmentQuestionCreateView,
    AssessmentUserCreateView,
    StartAssessmentView
)

urlpatterns = [
    path('', CreateAssessmentView.as_view(), name='create_assessment'),
    path('<str:pk>', AssessmentDetailView.as_view(), name='assessment_detail'),
    path('<str:pk>/questions', AssessmentQuestionCreateView.as_view(), name='create_assessment_question'),
    path('<str:pk>/session', AssessmentUserCreateView.as_view(), name='create_assessment_user'),
    path('<str:pk>/question', StartAssessmentView.as_view(), name='start_assessment'),
]