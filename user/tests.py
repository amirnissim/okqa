# encoding: utf-8
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.test import TestCase

from .models import *

class UserTest(TestCase):
    def test_register(self):
        c = Client()
        response = c.post(reverse('registration_register'),
                          {'username': u'משה',
                           'email':'info@example.com',
                           'password1':'123',
                           'password2':'123'})
        self.assertEquals(response.status_code, 200)
