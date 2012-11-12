from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _
from django.contrib.syndication.views import Feed
from django.contrib.auth.models import User
from okqa.qa.models import Answer

class RssUserAnswerFeed(Feed):
    """"Give candidate, get all answers for that candidate"""

    def get_object(self, request, candidate_id):
        return get_object_or_404(User, pk=candidate_id)

    def title(self, obj):
        return _('Answers by') + '%s' % obj.get_full_name()

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return _('Get all answers by') + '%s' % obj.get_full_name()

    def items(self, obj):
        return Answer.objects.filter(author=obj).order_by('-updated_at')

class AtomUserAnswerFeed(RssUserAnswerFeed):
    feed_type = Atom1Feed
    subtitle = RssUserAnswerFeed.description

