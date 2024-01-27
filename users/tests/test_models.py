from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertEqual(self.user.user_type, 'participant')
        self.assertEqual(self.user.bio, '')
        self.assertIsNone(self.user.birth_date)
        self.assertEqual(self.user.profile_picture, 'avatar.svg')

    def test_str_representation(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_type_choices(self):
        for choice in dict(get_user_model().USER_TYPE_CHOICES).keys():
            self.user.user_type = choice
            self.user.save()
            self.assertEqual(self.user.user_type, choice)

    def test_default_user_type(self):
        self.assertEqual(self.user.user_type, 'participant')
