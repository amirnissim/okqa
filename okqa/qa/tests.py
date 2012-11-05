from django.contrib.auth.models import User, AnonymousUser, Permission
from django.contrib.sites.models import Site
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.test import TestCase

from .models import *

class QuestionTest(TestCase):
    def setUp(self):
        self.common_user = User.objects.create_user("commoner", 
                                "commmon@example.com", "pass")
        self.candidate_user = User.objects.create_user("candidate", 
                                "candidate@example.com", "pass")
        add_answer = Permission.objects.get(codename="add_answer")
        self.candidate_user.user_permissions.add(add_answer)
        self.q = Question.objects.create(author = self.common_user,
                        subject="why?")
        self.a = self.q.answers.create(author = self.candidate_user,
                        content="because the world is round")
        self.site1 = Site.objects.create(domain='abc.com')
        self.site2 = Site.objects.create(domain='fun.com')
        self.q.tags.create(name="abc")
        self.q.tags.create(name="def")

    def test_sites(self):
        I = Site.objects.get_current()
        self.assertEqual(Question.on_site.count(), 1)
        self.assertEqual(Answer.on_site.count(), 1)

    def test_upvote(self):
        c = Client()
        response = c.post(reverse('upvote_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 302)
        response = c.post(reverse('auth_login'), dict(username='candidate',
                                                 password='pass'))
        self.assertEquals(response.status_code, 302)
        response = c.post(reverse('upvote_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "2")
        response = c.post(reverse('upvote_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 403)


        response = c.post(reverse('auth_logout'))
        response = c.post(reverse('auth_login'), dict(username='commoner',
                                                 password='pass'))
        self.assertEquals(response.status_code, 302)
        response = c.post(reverse('upvote_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 403)

        '''
        upvote = QuestionUpvote.objects.create(question=self.q, user=user)
        #TODO: use signals so the next line won't be necesary
        increase_rating(self.q)
        self.assertEquals(self.q.rating, 1)
        '''

    def test_repr(self):
        self.assertEqual("why?", unicode(self.q))

    def test_permissions(self):
        self.assertFalse(self.q.can_answer(self.common_user))
        self.assertTrue(self.q.can_answer(self.candidate_user))

    def tearDown(self):
        self.q.delete()
        User.objects.all().delete()
