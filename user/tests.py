from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser, Permission
from django.contrib.sites.models import Site
from social_auth.tests.client import SocialClient
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.test import TestCase

from .models import *

class UserTest(TestCase):
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
        self.user = User.objects.create_user("user", 
                                "user@example.com", "pass")
    def test_avatar(self):
        avatar_url = self.user.profile.avatar_url()
        self.assertTrue(avatar_url.startswith('http://www.gravatar.com/avatar/'))
        self.user.profile.avatar_uri = 'http://myavatar.com'
        self.user.profile.save()
        avatar_url = self.user.profile.avatar_url()
        self.assertEquals(avatar_url, 'http://myavatar.com')

    def test_candidate_list(self):
        c = Client()
        response = c.get(reverse('candidate_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user/candidate_list.html")
        self.assertFalse(response.context['candidates'])
        candidate_group = Group.objects.get(name='candidates')
        candidate_group.user_set.add(self.user)
        response = c.get(reverse('candidate_list'))
        self.assertEquals(len(response.context['candidates']), 1)

    def user_detail(self):
        c = Client()
        response = c.get(reverse('user_detail', {'slug': "user"}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user/candidate_detail.html")

    def test_invitation(self):
        user = Profile.objects.invite(username = "john",
                            email = "john@example.com",
                            first_name = "John",
                            last_name = "Doe",
                            site = Site.objects.get(pk=settings.SITE_ID)
                            )


    def tearDown(self):
        User.objects.all().delete()
