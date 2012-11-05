from datetime import date
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

# Create your models here.
class Party(models.Model):
    site = models.ForeignKey(Site)
    logo = models.ImageField(upload_to='logos')
    first_in_list = models.ForeignKey(User, null=True, blank=True)
    url = models.URLField(_('Home page'))
    primaries_date = models.DateField(_('Primaries Date'), null=True)
    qualifying_date = models.DateField(_('Qualifying date'), null=True)
    number_of_members = models.IntegerField(_('Number of party members'), null=True)
    open_knesset_id = models.IntegerField(null=True)

def handle_site_save(sender, created, instance, **kwargs):
    if created and instance._state.db=='default':
        Party.objects.create(site=instance)
post_save.connect(handle_site_save, sender=Site)
