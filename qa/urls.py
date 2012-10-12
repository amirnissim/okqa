from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'qa.views.home'),
    (r'^/$', 'qa.views.home'),
    (r'^q/$', 'qa.views.questions'),
    (r'^q/(?P<q_id>\d+)/$', 'qa.views.view_question'),
    (r'^add_answer/(?P<q_id>\d+)/$', 'qa.views.add_answer'),

    (r'^candidates/$', 'qa.views.candidates'),
    (r'^candidate/(?P<candidate_id>\d+)/$', 'qa.views.view_candidate'),

    (r'^voters/$', 'qa.views.voters'),
    (r'^voter/(?P<voter_id>\d+)/$', 'qa.views.view_voter'),
)
