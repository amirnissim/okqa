from django.contrib.auth.models import User, AnonymousUser, Permission
from django.contrib.sites.models import Site
from social_auth.tests.client import SocialClient
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import translation

from django.test import TestCase

from entities.models import Domain, Division, Entity
from qa.models import Question, Answer

class QuestionTest(TestCase):

    def setUp(self):
        domain = Domain.objects.create(name="test")
        division = Division.objects.create(name="localities", domain=domain)
        entity = Entity.objects.create(name="the moon", division=division)
        self.common_user = User.objects.create_user("commoner", 
                                "commmon@example.com", "pass")
        self.candidate_user = User.objects.create_user("candidate", 
                                "candidate@example.com", "pass")
        self.candidate_user.profile.locality = entity
        self.candidate_user.profile.is_candidate = True
        self.candidate_user.profile.save()
        self.editor_user = User.objects.create_user("editor", 
                                "editor@example.com", "pass")
        self.editor_user.profile.locality = entity
        self.editor_user.profile.is_editor = True
        self.editor_user.profile.save()
        self.q = Question.objects.create(author = self.common_user,
                        subject="why?", entity=entity)
        self.a = self.q.answers.create(author = self.candidate_user,
                        content="because the world is round")
        self.site1 = Site.objects.create(domain='abc.com')
        self.site2 = Site.objects.create(domain='fun.com')
        self.q.tags.create(name="abc")
        self.q.tags.create(name="def")
        translation.deactivate_all()

    def test_home_view(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['questions'].count(), 1)

    def tearDown(self):
        self.q.delete()
        User.objects.all().delete()
