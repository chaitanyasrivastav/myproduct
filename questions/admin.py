from django.contrib import admin

# Register your models here.
from .models import Question, Answer, Choice

class QuestionAdmin(admin.ModelAdmin):
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Choice)
