import urllib, hashlib, datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group, Permission
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext as _

from taggit.managers import TaggableManager
from registration.models import RegistrationProfile
from entities.models import Entity

NOTIFICATION_PERIOD_CHOICES = (
    (u'N', _('No Email')),
    (u'D', _('Daily')),
    (u'W', _('Weekly')),
)
GENDER_CHOICES = (
    (u'M', _('Male')),
    (u'F', _('Female')),
)

NEVER_SENT = datetime.datetime(1970,8,6)

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
    def candidates_for_entity(self, entity_slug):
        ''' get all the candidates in an entity '''
        return User.objects.filter(profile__locality__slug = entity_slug,
                                   profile__is_candidate=True)

class Profile(models.Model):
    # TODO: chnage OneToOne
    user = models.OneToOneField(User, related_name='profile')
    public_profile = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(null=True,blank=True)
    email_notification = models.CharField(max_length=1, choices=NOTIFICATION_PERIOD_CHOICES, blank=True, null=True, default='D')
    avatar_uri = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    last_email_update = models.DateTimeField(default=NEVER_SENT)
    locality = models.ForeignKey(Entity, null=True, verbose_name=_('Locality'))
    sites = models.ManyToManyField(Site)
    is_candidate = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    on_site = CurrentSiteManager()

    objects = ProfileManager()
    def avatar_url(self, size=40):
        if self.avatar_uri:
            return self.avatar_uri
        ''' getting the avatar image url from Gravatar '''
        default = "http://oshot.hasadna.org.il/static/img/defaultavatar.png"
        email = self.user.email
        if self.avatar_uri:
            return self.avatar_uri

        if email:
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
            return gravatar_url
        else:
            return default

def handle_user_save(sender, created, instance, **kwargs):
    if created: # and instance._state.db=='default':
        Profile.objects.create(user=instance)
post_save.connect(handle_user_save, sender=User)
