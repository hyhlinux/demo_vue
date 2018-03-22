from unittest import TestCase
from .user import User

class TestUser(TestCase):
    def setUp(self):
        self.user = User(email="hyhliunx@163.com", password="123456")
        self.user.save(force_insert=True)

    def test_passwd(self):
        self.assertEqual(self.user.password, "123456")

    def test_email(self):
        self.assertEqual(self.user.email, "hyhliunx@163.com")

    def test_find(self):
        User.objects.filter()
        user_list = User.objects.fi()
        for user in user_list:
            print(user.email, user.password)

    def tearDown(self):
        self.user = None
