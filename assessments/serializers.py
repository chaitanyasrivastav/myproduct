from rest_framework import serializers
from questions.serializers import ChoiceContentSerializer

from questions.models import Question

from .models import Assessment, AssessmentQuestionJunction, AssessmentUserJunction
  
class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = "__all__"

class AssessmentQuestionJunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestionJunction
        fields = "__all__"

class AssessmentUserJunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentUserJunction
        fields = "__all__"

class StartAssessmentSerializer(serializers.ModelSerializer):
    options = ChoiceContentSerializer(many=True)
    class Meta:
        model = Question
        fields = ["title", "content", "options"]