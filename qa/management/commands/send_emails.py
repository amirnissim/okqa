# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from django.core.urlresolvers import reverse
from user.models import invite_user
from qa.models import Question
from user.models import Profile

import ucsv as csv

class Command(BaseCommand):
    args = '<members_file>'
    help = 'import members from a csv file'

    def handle (self, *args, **options):
        site = Site.objects.get(pk=settings.SITE_ID)
        # TODO: get only new questions and questions with new answers
        context = dict(questions=Question.on_site.all(),
                       header="Hello there!",
                       )
        for profile in Profile.on_site.all():
            user = profile.user
            if user.is_active:
                context['header'] = '''שלומות,

הנה מה שחדש באתר שלנו.
'''
                context['last_sent'] = user.profile.last_email_update
                template = "qa/email_update.html"
                subject = _("update from %s") % site.name
            else:

                ''' send an invitation email '''
                reg_profile = user.registrationprofile_set.all()[0]
                ctx_dict = {'invitation_key': reg_profile.activation_key,
                            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                            'site': site}
                subject = render_to_string('user/invitation_email_subject.txt',
                        ctx_dict).rstrip()
                # Email subject *must not* contain newlines
            html_content = render_to_string(template, context)
            # TODO: create a link for the update and send it to shaib
            text_content = 'Sorry, we only support html based email'
            # create the email, and attach the HTML version as well.
            # TODO: optimize to send the same message to all users on the cycle
            msg = EmailMultiAlternatives(subject, text_content,
                    settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
