from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('okqa.qa.views',
    url(r'^/?$', 'questions', name='home'),

    url(r'^q/(?P<q_id>\d+)/$', 'view_question', name='question-details'),

    url(r'^candidates/$', 'candidates', name='candidates'),
    (r'^candidate/(?P<candidate_id>\d+)/$', 'view_candidate'),

    url(r'^members/$', 'members', name='members'),
    (r'^members/(?P<member_id>\d+)/$', 'view_member'),

    (r'^add_answer/(?P<q_id>\d+)/$', 'add_answer'),
    (r'^add_question/$', 'add_question'),
    (r'^upvote_question/(?P<q_id>\d+)/$', 'upvote_question'),

)
