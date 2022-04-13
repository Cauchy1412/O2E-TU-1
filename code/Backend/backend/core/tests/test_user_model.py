import unittest
from core.models.user import User
from django.contrib import admin


class TestUserModel(unittest.TestCase):
    fixtures = ['initial.json', 'users.json']

    def setUp(self) -> None:
        print("test user model")

    def tearDown(self) -> None:
        print("test over")

    def test_user_name(self):
        print("test user attribute")
        user = User.objects.get(pk=10001)
        self.assertEqual(user.username, "test_user_1")

    def test_user_follow(self):
        print("test user follow and unfollow method")
        user1 = User.objects.get(pk=10001)
        user2 = User.objects.get(pk=10002)
        self.assertTrue(user1.follow_by_id(user2.id))
        self.assertEqual(len(user2.get_fan()), 1)
        self.assertTrue(user1.unfollow_by_id(user2.id))
        self.assertEqual(len(user2.get_fan()), 0)
