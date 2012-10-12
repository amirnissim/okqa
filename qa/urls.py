from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'qa.views.home'),
    (r'^q/$', 'qa.views.list_questions'),
    (r'^q/(?P<q_id>\d+)/$', 'qa.views.view_question'),
    (r'^add_answer/(?P<q_id>\d+)/$', 'qa.views.add_answer'),

)
