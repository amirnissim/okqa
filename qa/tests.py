from django.contrib.auth.models import User, AnonymousUser, Permission
from django.contrib.sites.models import Site
from social_auth.tests.client import SocialClient
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.test import TestCase

from entities.models import Domain, Division, Entity
from .models import *

class QuestionTest(TestCase):
    client = SocialClient
    user = {
        'first_name': 'Django',
        'last_name': 'Reinhardt',
        'verified': True,
        'name': 'Django Reinhardt',
        'locale': 'en_US',
        'hometown': {
            'id': '12345678',
            'name': 'Any Town, Any State'
        },
        'expires': '4812',
        'updated_time': '2012-01-29T19:27:32+0000',
        'access_token': 'dummyToken',
        'link': 'http://www.facebook.com/profile.php?id=1234',
        'location': {
            'id': '108659242498155',
            'name': 'Chicago, Illinois'
        },
        'gender': 'male',
        'timezone': -6,
        'id': '1234',
        'email': 'user@domain.com'
    }
    def setUp(self):
        domain = Domain.objects.create(name="test")
        division = Division.objects.create(name="localities", domain=domain)
        entity = Entity.objects.create(name="the moon", division=division)
        self.common_user = User.objects.create_user("commoner", 
                                "commmon@example.com", "pass")
        self.candidate_user = User.objects.create_user("candidate", 
                                "candidate@example.com", "pass")
        self.candidate_user.profile.locality = entity
        self.candidate_user.profile.save()
        self.candidate_user.profile.set_candidate(True)
        self.q = Question.objects.create(author = self.common_user,
                        subject="why?", entity=entity)
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
        #TODO: self.assertEqual(TaggedQuestion.on_site.count(), 1)

    def test_permissions(self):
        self.assertFalse(self.q.can_answer(self.common_user))
        self.assertTrue(self.q.can_answer(self.candidate_user))

    def test_question_detail(self):
        c = Client()
        q_url = reverse('question_detail',
                         kwargs={'entity_slug': self.q.entity.slug, 'slug':self.q.unislug})

        response = c.get(q_url)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.context['can_answer'])
        self.assertTemplateUsed(response, "qa/question_detail.html")
        self.assertTrue(c.login(username="candidate", password="pass"))
        response = c.get(q_url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context['can_answer'])

    def test_flag(self):
        self.q.flagged()
        self.assertEquals(self.q.flags_count, 1)
        c = Client()
        response = c.post(reverse('flag_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 403)
        respone = c.post(reverse('login'),
                {'username':"commoner", 'password':"pass"})
        response = c.post(reverse('flag_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "2")
        self.q = Question.objects.get(pk=self.q.id)
        self.assertEquals(self.q.flags_count, 2)
        response = c.post(reverse('flag_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 403)

    def test_upvote(self):
        c = SocialClient()
        response = c.post(reverse('upvote_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 302)
        c.login(self.user, backend='facebook')
        response = c.post(reverse('upvote_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "2")
        response = c.post(reverse('upvote_question', kwargs={'q_id':self.q.id}))
        self.assertEquals(response.status_code, 403)

    def test_repr(self):
        self.assertEqual("why?", unicode(self.q))

    def tearDown(self):
        self.q.delete()
        User.objects.all().delete()
