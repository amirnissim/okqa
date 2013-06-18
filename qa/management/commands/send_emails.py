# -*- coding: utf-8 -*-
import sys
import urlparse
from datetime import datetime,timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _

from django.core.urlresolvers import reverse
from user.models import invite_user
from qa.models import Question
from user.models import Profile, NEVER_SENT
from flatblocks.models import FlatBlock

class Command(BaseCommand):
    args = '[username1 username2 ...]'
    help = 'send email updates to users that want it'

    diffs = dict(D=timedelta(0, 23*3600),
                 W=timedelta(0, (23+6*24)*3600))

    def handle (self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        now = datetime.now()
        if len(args):
            qs = Profile.on_site.filter(user__email=args)
        else:
            qs = Profile.on_site.all()
        site = Site.objects.get(pk=settings.SITE_ID)
        # TODO: get only new questions and questions with new answers
        context = {'questions': Question.on_site.all().order_by('-updated_at'),
                   'header': "Hello there!",
                   'ROOT_URL': 'http://' + site.domain
                   }
        for profile in qs:
            user = profile.user
            last_sent = user.profile.last_email_update
            try:
                freq = self.diffs[user.profile.email_notification]
            except KeyError:
                freq = sys.maxint

            if user.is_active and now-last_sent > freq:
                header = "email.update_header"
                template = "qa/email_update.html"
            elif not user.is_active:
                ''' send an invitation email '''
                reg_profile = user.registrationprofile_set.all()[0]
                if reg_profile.activation_key_expired() and last_sent==NEVER_SENT:
                    # create a new registration key and send an update
                    header = "email.inactive_header"
                    context['key'] = reg_profile.activation_key
                    context['email'] = user.username
                    subject = _("update from %(name)s") % site
                    # reset the key duration, giving the user more time
                    user.date_joined = now
                    user.save()

                ctx_dict = {'invitation_key': reg_profile.activation_key,
                            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                            'site': site}
                subject = render_to_string('user/invitation_email_subject.txt',
                        ctx_dict).rstrip()
                 # Email subject *must not* contain newlines
            else:
                continue
            context['last_sent'] = last_sent
            context['header'] = header
            context['footer'] = 'email.footer'
            subject = '%s | %s' % (site.name,
                    FlatBlock.objects.get(slug=header).header.rstrip())
            html_content = render_to_string("qa/email_update.html", context)
            # TODO: create a link for the update and send it to shaib
            text_content = 'Sorry, we only support html based email'
            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content,
                    settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
