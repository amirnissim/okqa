from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('okqa.qa.views',
    url(r'^/?$', 'questions', name='home'),

    url(r'^q/(?P<q_id>\d+)/$', 'view_question', name='question-details'),

    url(r'^candidates/$', 'candidates', name='candidates'),
    (r'^candidate/(?P<candidate_id>\d+)/$', 'view_candidate'),

    url(r'^members/$', 'members', name='members'),
    (r'^members/(?P<member_id>\d+)/$', 'view_member'),

    url(r'^add_answer/(?P<q_id>\d+)/$', 'post_answer', name='post_answer'),
    (r'^add_question/$', 'add_question'),
    (r'^upvote_question/(?P<q_id>\d+)/$', 'upvote_question'),
	
	url(r'^tags/(?P<tags>[\w,]+)/$', 'tagged_questions'),

)
