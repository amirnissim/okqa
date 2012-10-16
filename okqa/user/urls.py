from django.conf.urls.defaults import patterns, include, url
from registration.views import register

urlpatterns = patterns('',
    url(r'^register/$', 
        register,
        {'backend': 'user.backends.RegBackend'},
        name='registration_register'),
    url(r'', include('registration.backends.default.urls')),
)
