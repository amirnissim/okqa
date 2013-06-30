from django.contrib import admin
from .models import *

class QuestionFlagAdmin(admin.StackedInline):
    model = QuestionFlag
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ QuestionFlagAdmin ]
    list_filter = ('flags_count',)

class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
