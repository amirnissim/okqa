from django.db import models
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

# Create your models here.
class Party(models.Model):
    site = models.ForeignKey(Site)
    logo = models.ImageField(upload_to='logos')
    first_in_list = models.ForeignKey(User, null=True, blank=True)
    url = models.URLField()
    primaries_date = models.DateField()
    qualifying_date = models.DateField()
    number_of_members = models.IntegerField()
    open_knesset_id = models.IntegerField()

def handle_site_save(sender, created, instance, **kwargs):
    if created and instance._state.db=='default':
        Party.objects.create(site=Site)
post_save.connect(handle_site_save, sender=Site)
