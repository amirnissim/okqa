from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('okqa.qa.views',
    url(r'^/?$', 'home', name='home'),

    url(r'^q/$', 'questions' ,name='questions'),
    (r'^q/(?P<q_id>\d+)/$', 'view_question'),

    url(r'^candidates/$', 'candidates', name='candidates'),
    (r'^candidate/(?P<candidate_id>\d+)/$', 'view_candidate'),

    url(r'^voters/$', 'voters', name='voters'),
    (r'^voter/(?P<voter_id>\d+)/$', 'view_voter'),

    (r'^add_answer/(?P<q_id>\d+)/$', 'add_answer'),
    (r'^add_question/$', 'add_question'),
    (r'^upvote_question/(?P<q_id>\d+)/$', 'upvote_question'),

)
