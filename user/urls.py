from django.conf.urls.defaults import patterns, include, url
from .views import *
from .feeds import *

urlpatterns = patterns('',
    url(r'^profile/$', edit_profile, name='edit_profile'),
    url(r'^(?P<entity_slug>.*)/candidates/$', candidate_list, name="candidate_list"),
    url(r'^users/(?P<slug>.+)/$', user_detail, name="candidate_detail"),
    url(r'^candidate/(?P<candidate_id>\d+)/atom/$',
        AtomUserAnswerFeed(),
        name='user_feed'
    ),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                                  {'next_page': '/'},
                                  name="logout"),
    url(r'^login/$', 'django.contrib.auth.views.login',
                                  name='login'),
    url(r'^invitation/(?P<invitation_key>\w+)/$',
        InvitationView.as_view(),
        name='accept-invitation'),
)
