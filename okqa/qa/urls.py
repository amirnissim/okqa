from django.conf.urls.defaults import patterns, url
from okqa.qa.sitemaps import sitemaps
from okqa.qa.views import RssQuestionFeed, RssQuestionAnswerFeed, RssUserAnswerFeed, AtomQuestionFeed, AtomQuestionAnswerFeed, AtomUserAnswerFeed

urlpatterns = patterns('',
    url(r'^/?$', 'okqa.qa.views.questions', name='home'),

    url(r'^q/(?P<q_id>\d+)/$', 'okqa.qa.views.view_question', name='question-details'),

    url(r'^candidates/$', 'okqa.qa.views.candidates', name='candidates'),
    (r'^candidate/(?P<candidate_id>\d+)/$', 'view_candidate'),

    url(r'^members/$', 'okqa.qa.views.members', name='members'),
    (r'^members/(?P<member_id>\d+)/$', 'okqa.qa.views.view_member'),

    url(r'^a/post/(?P<q_id>\d+)/$', 'okqa.qa.views.post_answer', name='post_answer'),
    url(r'^q/post/$', 'okqa.qa.views.post_question', name='post_question'),
    url(r'^upvote_question/(?P<q_id>\d+)/$', 'okqa.qa.views.upvote_question', name='upvote_question'),
    url(r'^tags/(?P<tags>.+)/$', 'okqa.qa.views.tagged_questions', name="show_tags"),
    #(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^feeds/rss/questions/$', RssQuestionFeed()),
    (r'^q/(?P<q_id>\d+)/feeds/rss/answers/$', RssQuestionAnswerFeed()),
    (r'^candidate/(?P<candidate_id>\d+)/feeds/rss/answers/$', RssUserAnswerFeed()),

    (r'^feeds/atom/questions/$', AtomQuestionFeed()),
    (r'^q/(?P<q_id>\d+)/feeds/atom/answers/$', AtomQuestionAnswerFeed()),
    (r'^candidate/(?P<candidate_id>\d+)/feeds/atom/answers/$', AtomUserAnswerFeed()),
)
