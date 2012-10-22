from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('okqa.qa.urls')),
    url(r'', include('okqa.user.urls')),
    url(r'accounts/', include('registration.backends.default.urls')),
    (r'^search/', include('haystack.urls')),
)
