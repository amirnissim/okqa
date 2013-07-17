from django.conf.urls.defaults import patterns, url
from .views import *
from qa.sitemaps import sitemaps

urlpatterns = patterns('qa.views',
    url(r'^(?P<entity_slug>.*)/qna/post_q/$', 'post_question', name='post_question'),
    url(r'^(?P<entity_slug>[-\w]+)/qna/(?P<slug>[-\w]+)/$',
        QuestionDetail.as_view(),
        name='question_detail'
    ),
    url(r'^(?P<entity_id>[-\d]+)/qna/$', 'questions', name='qna'),
    url(r'^(?P<entity_slug>[-\w]+)/qna/$', 'questions', name='qna'),
    url(r'^(?P<entity_slug>[-\w]+)/qna/tags/(?P<tags>.+)/$', 'questions', name='show_tags'),

    url(r'^qna/post_a/(?P<q_id>\d+)/$', 'post_answer', name='post_answer'),

	url(r'^qna/flag_question/(?P<q_id>\d+)/flag/$', 'flag_question', name='flag_question'),

    url(r'upvote_question/(?P<q_id>\d+)/$', 'upvote_question', name='upvote_question'),
)

urlpatterns += patterns('',
    (r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.index',
        {'sitemaps': sitemaps}
    ),

    (r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}
    ),

    url(r'^qna/rss/$',
        RssQuestionFeed(),
        name='rss_all_questions'
    ),

    url(r'^(?P<entity>.*)/qna/atom/$',
        AtomQuestionFeed(),
        name='atom_entity_questions'
    ),

    url(r'^atom/$',
        AtomQuestionFeed(),
        name='atom_all_questions'
    ),

    url(r'^q/(?P<q_id>\d+)/rss/answers/$',
        RssQuestionAnswerFeed(),
        name='rss_question_answers'
    ),

    url(r'^q/(?P<q_id>\d+)/atom/answers/$',
        AtomQuestionAnswerFeed(),
        name='atom_question_answers'
    ),
)
