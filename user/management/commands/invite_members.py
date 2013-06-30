# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from django.core.urlresolvers import reverse
from user.models import invite_user

import ucsv as csv

class Command(BaseCommand):
    args = '<members_file>'
    help = 'import members from a csv file'

    def handle (self, *args, **options):
        file_name=args[0]
        f = open(file_name, 'rb')
        d = csv.DictReader(f)
        site = Site.objects.get(pk=settings.SITE_ID)
        for row in d:
            names = row[u'שם'].split(' ')
            email = row[u'דואר אלקטרוני']
            user = invite_user(
                    username = email,
                    email = email,
                    first_name = names[0],
                    last_name = ' '.join(names[1:]),
                    site = site,
                    )
            if user.is_active:
                self.stdout.write('%s is already active, no invitation sent' % email)
            else:
                ''' send an invitation email '''
                reg_profile = user.registrationprofile_set.all()[0]
                ctx_dict = {'invitation_key': reg_profile.activation_key,
                            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                            'site': site}
                subject = render_to_string('user/invitation_email_subject.txt',
                        ctx_dict).rstrip()
                # Email subject *must not* contain newlines
                html_content = render_to_string('user/invitation_email.html',
                                           ctx_dict)
                text_content = '\n'.join((strip_tags(html_content),
                    "http://%s%s" % (site.domain,
                                     reverse("accept-invitation", 
                                             args=(ctx_dict['invitation_key'], )))))

                # create the email, and attach the HTML version as well.
                msg = EmailMultiAlternatives(subject, text_content,
                        settings.DEFAULT_FROM_EMAIL, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
