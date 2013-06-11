# -*- coding: utf-8 -*-
import ucsv as csv
from djano.conf import setting
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from registration.models import RegistrationProfile
from models import User

class Command(BaseCommand):
    args = '<member_file>'
    help = 'import members from a csv file'

    def handle (self, *args, **options):
        file_name=args[0]
        f = open(file_name, 'rb')
        d = csv.DictReader(f)
        for row in d:
            names = row[u'שם'].split(' ')
            email = row[u'דואר אלקטרוני']
            user = Profile.objects.invite(
                    username = email,
                    email = email,
                    first_name = names[0],
                    last_name = ' '.join(names[1:]),
                    site = Site.objects.get(pk=settings.SITE_ID)
                    )
            ''' send an invitation email '''
