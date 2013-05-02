from django.conf.urls.defaults import patterns, include, url
from .views import *
from .feeds import *
from .forms import UserRegistrationForm

urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),
    url(r'^profile/$', edit_profile, name='edit_profile'),
    url(r'^candidates/$', candidate_list, name="candidate_list"),
    url(r'^candidates/activate/(?P<activation_key>\w+)/$',
        candidate_activate,
        name='candidate_activate'),
    (r'^candidates/accounts/', include('user.candidate_registration_backend.urls')),
    url(r'^users/(?P<slug>.+)/$', user_detail, name="candidate_detail"),

    url(r'^candidate/(?P<candidate_id>\d+)/atom/$',
        AtomUserAnswerFeed(),
        name='user_feed'
    ),
)
