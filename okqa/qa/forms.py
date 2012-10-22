from django.forms import ModelForm
from models import Answer, Question

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ("content",)

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ("subject", "content", "tags", )

