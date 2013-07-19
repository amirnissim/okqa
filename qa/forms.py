from django.forms import ModelForm, TextInput, Textarea, HiddenInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from models import Answer, Question

from slugify import slugify as unislugify


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ("content",)


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        # fields = ("subject", "content", "tags", )
        fields = ("subject", "entity")
        widgets = { 'subject': Textarea(attrs={'cols': 70, 'rows': 2}), 
                    'entity': HiddenInput}

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        unislug = unislugify(cleaned_data.get('subject'))
        if Question.objects.filter(entity=cleaned_data['entity']).filter(unislug=unislug):
            raise ValidationError(_("Question already exists."))

        return cleaned_data
