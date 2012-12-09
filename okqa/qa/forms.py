from django.forms import ModelForm, TextInput, Textarea
from models import Answer, Question

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ("content",)

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        # fields = ("subject", "content", "tags", )
        fields = ("subject", )
        widgets = { 'subject': Textarea(attrs={'cols': 70, 'rows': 2}), }

