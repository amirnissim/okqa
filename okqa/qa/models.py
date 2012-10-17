from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from taggit.managers import TaggableManager

MAX_LENGTH_Q_SUBJECT = 255
MAX_LENGTH_Q_CONTENT = 255

MAX_LENGTH_A_SUBJECT = 255
MAX_LENGTH_A_CONTENT = 255

CANDIDATES_GROUP_NAME = "candidates"

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class Question(BaseModel):
    author = models.ForeignKey(User, related_name="questions", verbose_name=_("author"))
    subject = models.CharField(_("subject"), max_length=MAX_LENGTH_Q_SUBJECT, help_text=_("subject"))
    content = models.TextField(_("content"), max_length=MAX_LENGTH_Q_CONTENT, help_text=_("content"))
    rating = models.IntegerField(_("rating"), default=0)
    tags = TaggableManager()

    def __unicode__(self):
        return self.subject

class Answer(BaseModel):
    author = models.ForeignKey(User, related_name="answers", verbose_name=_("author"))
    content = models.TextField(_("content"), max_length=MAX_LENGTH_A_CONTENT, help_text=_("content"))
    rating = models.IntegerField(_("rating"), default=0)
    question = models.ForeignKey(Question, related_name="answers", verbose_name=_("question"))

class QuestionUpvote(BaseModel):
    question = models.ForeignKey(Question, related_name="upvotes")
    user = models.ForeignKey(User, related_name="upvotes")
