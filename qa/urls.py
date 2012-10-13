from django.conf.urls.defaults import patterns
from qa import views

urlpatterns = patterns('',
    (r'^home', views.home),
    (r'^create', views.create_user),
    (r'^profile', views.user_profile),
)
