import urllib, hashlib
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group

from taggit.managers import TaggableManager
from registration.models import RegistrationProfile

NOTIFICATION_PERIOD_CHOICES = (
    (u'N', _('No Email')),
    (u'D', _('Daily')),
    (u'W', _('Weekly')),
)
GENDER_CHOICES = (
    (u'M', _('Male')),
    (u'F', _('Female')),
)

def invite_user(site, username, email, first_name="", last_name=""):
    ''' invite a new user to the system '''
    user, created = User.objects.get_or_create(username=username,
            defaults = {'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                       })
    if created:
        user.is_active = False
        user.save()
    elif user.is_active:
        return user
    else:
        user.registrationprofile_set.all().delete()


    registration_profile = RegistrationProfile.objects.create_profile(user)

    return user

class ProfileManager(models.Manager):
    def candidates(self):
        candidate_group, candidate_group_created = Group.objects.get_or_create(name="candidates")
        return candidate_group.user_set.all().\
                annotate(num_answers=models.Count('answers')).order_by("-num_answers")

class Profile(models.Model):
    # TODO: chnage OneToOne
    user = models.OneToOneField(User, related_name='profile')
    public_profile = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(null=True,blank=True)
    email_notification = models.CharField(max_length=1, choices=NOTIFICATION_PERIOD_CHOICES, blank=True, null=True, default='D')
    avatar_uri = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    objects = ProfileManager()
    def avatar_url(self, size=40):
        if self.avatar_uri:
            return self.avatar_uri
        ''' getting the avatar image url from Gravatar '''
        default = "http://okqa.herokuapp.com/static/img/defaultavatar.png"
        email = self.user.email
        if self.avatar_uri:
            return self.avatar_uri

        if email:
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
            return gravatar_url
        else:
            return default

    def set_can_answer(self, can_answer):
        candidate_group, created = Group.objects.get_or_create(name="candidates")
        if can_answer:
            self.user.groups.add(candidate_group)
        else:
            self.user.groups.remove(candidate_group)

def handle_user_save(sender, created, instance, **kwargs):
    if created and instance._state.db=='default':
        Profile.objects.create(user=instance)
post_save.connect(handle_user_save, sender=User)
