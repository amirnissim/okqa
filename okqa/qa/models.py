from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

MAX_LENGTH_Q_SUBJECT = 80
MAX_LENGTH_Q_CONTENT = 255

MAX_LENGTH_A_SUBJECT = 80
MAX_LENGTH_A_CONTENT = 500

CANDIDATES_GROUP_NAME = "candidates"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TaggedQuestion(TaggedItemBase):
    content_object = models.ForeignKey("Question")


class Question(BaseModel):
    author = models.ForeignKey(User, related_name="questions", verbose_name=_("author"))
    subject = models.CharField(_("subject"), max_length=MAX_LENGTH_Q_SUBJECT,
        help_text=_("Please enter a subject in no more than %s letters") % MAX_LENGTH_Q_SUBJECT)
    content = models.TextField(_("content"), max_length=MAX_LENGTH_Q_CONTENT,
        help_text=_("Please enter your content in no more than %s letters") % MAX_LENGTH_Q_CONTENT)
    rating = models.IntegerField(_("rating"), default=1)
    tags = TaggableManager(through=TaggedQuestion)

    def __unicode__(self):
        return self.subject

    def can_answer(self, user):
        ''' Can a given user answer self? '''
        return user.has_perm('qa.add_answer')

    def get_absolute_url(self):
        return reverse('question-details', kwargs={'q_id': self.id})


class Answer(BaseModel):
    author = models.ForeignKey(User, related_name="answers", verbose_name=_("author"))
    content = models.TextField(_("content"), max_length=MAX_LENGTH_A_CONTENT,
        help_text=_("Please enter an answer in no more than %s letters") % MAX_LENGTH_A_CONTENT)
    rating = models.IntegerField(_("rating"), default=0)
    question = models.ForeignKey(Question, related_name="answers", verbose_name=_("question"))

    def __unicode__(self):
        return "%s: %s" % (self.author, self.content[:30])

    def get_absolute_url(self):
        return reverse('question-details', kwargs={'q_id': self.question.id})


class QuestionUpvote(BaseModel):
    question = models.ForeignKey(Question, related_name="upvotes")
    user = models.ForeignKey(User, related_name="upvotes")
