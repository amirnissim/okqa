from django.contrib.auth.models import User, AnonymousUser, Permission

from django.test import TestCase

from models import Question

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

    def test_repr(self):
        self.assertEqual("why?", unicode(self.q))

    def test_permissions(self):
        self.assertFalse(self.q.can_answer(self.common_user))
        self.assertTrue(self.q.can_answer(self.candidate_user))

    def tearDown(self):
        self.q.delete()
        User.objects.all().delete()
