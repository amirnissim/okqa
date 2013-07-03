from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from taggit.models import TaggedItemBase
from slugify import slugify as unislugify
from taggit_autosuggest.managers import TaggableManager
from entities.models import Entity


MAX_LENGTH_Q_SUBJECT = 140
MAX_LENGTH_Q_CONTENT = 255

MAX_LENGTH_A_SUBJECT = 80
MAX_LENGTH_A_CONTENT = 500

class BaseModel(models.Model):
    ''' just a common time base for the models
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# TODO: next class looks silly, do we really need it?
class TaggedQuestion(TaggedItemBase):
    content_object = models.ForeignKey("Question")
    sites = models.ManyToManyField(Site)
    # objects = models.Manager()
    # objects = CurrentSiteManager()

class Question(BaseModel):

    unislug = models.CharField(
        _('unicode slug'),
        max_length=MAX_LENGTH_Q_SUBJECT,
        null=True,
        blank=True,
        editable=False
    )
    author = models.ForeignKey(User, related_name="questions", verbose_name=_("author"))
    subject = models.CharField(_("question"), max_length=MAX_LENGTH_Q_SUBJECT,
        help_text=_("Please enter a subject in no more than %s letters") % MAX_LENGTH_Q_SUBJECT)
    content = models.TextField(_("details"), max_length=MAX_LENGTH_Q_CONTENT,
       help_text=_("Please enter your content in no more than %s letters") % MAX_LENGTH_Q_CONTENT,
       blank = True, default = '')
    rating = models.IntegerField(_("rating"), default=1)
    flags_count = models.IntegerField(_("flags counter"), default=0)
    tags = TaggableManager(through=TaggedQuestion)
    # tags = TaggableManager(through=TaggedQuestion, blank=True)
    sites = models.ManyToManyField(Site)
    # for easy access to current site questions
    objects = models.Manager()
    on_site = CurrentSiteManager()
    entity = models.ForeignKey(Entity, null=True, related_name="questions")

    def __unicode__(self):
        return self.subject

    def can_answer(self, user):
        ''' Can a given user answer self? '''
        return user.has_perm('qa.add_answer')

    def get_absolute_url(self):
        return reverse('question_detail', kwargs=dict(entity=self.entity.slug,
                                                       slug=self.unislug))

    def save(self, **kwargs):
        # make a unicode slug from the subject
        self.unislug = unislugify(self.subject)
        return super(Question, self).save(**kwargs)

    @transaction.commit_on_success
    def flagged(self):
        self.flags_count += 1
        self.save()
        return self.flags_count


class Answer(BaseModel):
    author = models.ForeignKey(User, related_name="answers", verbose_name=_("author"))
    content = models.TextField(_("content"), max_length=MAX_LENGTH_A_CONTENT,
        help_text=_("Please enter an answer in no more than %s letters") % MAX_LENGTH_A_CONTENT)
    rating = models.IntegerField(_("rating"), default=0)
    question = models.ForeignKey(Question, related_name="answers", verbose_name=_("question"))
    sites = models.ManyToManyField(Site)
    # for easy access to current site answers
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return "%s: %s" % (self.author, self.content[:30])

    def get_absolute_url(self):
        return '%s#answer-%s' % (self.question.get_absolute_url(), self.id)

class QuestionUpvote(BaseModel):
    question = models.ForeignKey(Question, related_name="upvotes")
    user = models.ForeignKey(User, related_name="upvotes")

class QuestionFlag(BaseModel):
    question = models.ForeignKey(Question, related_name="flags")
    reporter = models.ForeignKey(User, related_name="flags")

''' signals code, to ensure correct site is saved 
'''
@receiver(post_save)
def saved(sender, created, instance, **kwargs):
    if sender in (Question, Answer, TaggedQuestion):
        instance.sites.add(Site.objects.get_current())

