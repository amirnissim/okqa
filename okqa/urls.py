from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin
from entities.views.ui import EntityDetail, EntityList

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', EntityList.as_view(), name="home"),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^robots\.txt',
        TemplateView.as_view(template_name='robots.txt')
    ),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'', include('qa.urls')),
    url(r'', include('user.urls')),
    url(r'', include('social_auth.urls')),
    (r'^(?P<entity>)/search/', include('search.urls')),
    (r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    # flat pages to help with static pages
    (r'^p/(?P<url>.*)$', 'django.contrib.flatpages.views.flatpage'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
