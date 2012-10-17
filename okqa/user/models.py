import urllib, hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from taggit.managers import TaggableManager

NOTIFICATION_PERIOD_CHOICES = (
    (u'N', _('No Email')),
    (u'D', _('Daily')),
    (u'W', _('Weekly')),
)
GENDER_CHOICES = (
    (u'M', _('Male')),
    (u'F', _('Female')),
)

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True, related_name='profiles')
    public_profile = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(null=True,blank=True)
    email_notification = models.CharField(max_length=1, choices=NOTIFICATION_PERIOD_CHOICES, blank=True, null=True)

    def avatar_url(self, size=40):
        ''' getting the avatar image url from Gravatar '''
        email = self.user.email

        default = "http://okqa.herokuapp.com/static/img/defaultavatar.png"

        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url
