"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

"""


from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from registration.views import RegistrationView
from django.contrib.auth.decorators import login_required

registration_closed_view = TemplateView.as_view(
        template_name='registration/registration_closed.html')

urlpatterns = patterns('',
                       url(r'^register/$',
                           login_required(RegistrationView.as_view()),
                           {'backend': 'user.candidate_registration_backend.CandidateBackend',
                            'template_name': 'user/add_candidate.html'},
                           name='candidate_register'),
                       url(r'^register/closed/$',
                           registration_closed_view,
                           name='candidate_registration_disallowed'),
                       )
