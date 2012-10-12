from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from taggit.managers import TaggableManager

MAX_LENGTH_Q_SUBJECT = 255
MAX_LENGTH_Q_CONTENT = 255

MAX_LENGTH_A_SUBJECT = 255
MAX_LENGTH_A_CONTENT = 255


class Question(models.Model):
    author = models.ForeignKey(User, related_name="questions")
    subject = models.CharField(max_length=MAX_LENGTH_Q_SUBJECT, help_text=_("subject"))
    content = models.TextField(max_length=MAX_LENGTH_Q_CONTENT, help_text=_("content"))
    tags = TaggableManager()

class Answer(models.Model):
    author = models.ForeignKey(User, related_name="answers")
    subject = models.CharField(max_length=MAX_LENGTH_A_SUBJECT, help_text=_("subject"))
    content = models.TextField(max_length=MAX_LENGTH_A_CONTENT, help_text=_("content"))

    question = models.ForeignKey(Question, related_name="answers")

