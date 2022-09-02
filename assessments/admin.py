from django.contrib import admin

from .models import Assessment, AssessmentQuestionJunction

# Register your models here.
admin.site.register(Assessment)
admin.site.register(AssessmentQuestionJunction)