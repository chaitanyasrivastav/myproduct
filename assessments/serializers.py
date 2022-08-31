from rest_framework import serializers

from .models import Assessment, AssessmentQuestionJunction
  
class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = "__all__"

class AssessmentQuestionJunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestionJunction
        fields = "__all__"