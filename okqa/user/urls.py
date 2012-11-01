from django.conf.urls.defaults import patterns, include, url
from registration.views import register
from views import *

urlpatterns = patterns('',
    url(r'^register/$', register, {'backend': 'okqa.user.backends.RegBackend'}, 
        name='registration_register'),
    url(r'^login/$', login, name='login'),
    url(r'^candidates/$', candidate_list, name="candidate_list"),
    url(r'^users/(?P<slug>.+)/$', user_detail, name="candidate_detail"),

)
