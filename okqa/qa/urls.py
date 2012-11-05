from django.conf.urls.defaults import patterns, url
from okqa.qa.sitemaps import sitemaps
from okqa.qa.views import RssQuestionFeed, RssQuestionAnswerFeed, RssUserAnswerFeed, AtomQuestionFeed, AtomQuestionAnswerFeed, AtomUserAnswerFeed, QuestionDetail

urlpatterns = patterns('',
    url(r'^/?$', 'okqa.qa.views.questions', name='home'),

    url(r'^q/(?P<q_id>\d+)/$', 'okqa.qa.views.view_question', name='question-details'),

    url(r'^q/(?P<slug>[-\w]+)/$',
        QuestionDetail.as_view(),
        name='question_detail'
    ),
    url(r'^a/post/(?P<q_id>\d+)/$', 'okqa.qa.views.post_answer', name='post_answer'),
    url(r'^q/post/$', 'okqa.qa.views.post_question', name='post_question'),
    url(r'^upvote_question/(?P<q_id>\d+)/$', 'okqa.qa.views.upvote_question', name='upvote_question'),
    url(r'^tags/(?P<tags>.+)/$', 'okqa.qa.views.tagged_questions', name="show_tags"),

    (r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.index',
        {'sitemaps': sitemaps}
    ),

    (r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}
    ),

    url(r'^rss/$',
        RssQuestionFeed(),
        name='rss_all_questions'
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

    url(r'^candidate/(?P<candidate_id>\d+)/rss/answers/$',
        RssUserAnswerFeed(),
        name='rss_user_answers'
    ),

    url(r'^candidate/(?P<candidate_id>\d+)/atom/answers/$',
        AtomUserAnswerFeed(),
        name='atom_users_answers'
    )
)
