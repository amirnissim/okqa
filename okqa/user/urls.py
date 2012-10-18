from django.conf.urls.defaults import patterns, include, url
from registration.views import register
from okqa.user.views import login

urlpatterns = patterns('',
    url(r'^register/$', 
        register,
        {'backend': 'okqa.user.backends.RegBackend'},
        name='registration_register'),
    url(r'^login/', login, name='auth_login'),
    url(r'', include('registration.backends.default.urls')),
)
