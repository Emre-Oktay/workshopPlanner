from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from users.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_GET(self):
        response = self.client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_login_GET(self):
        response = self.client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_profile_GET(self):
        test_user = User.objects.create_user(
            username='testuser', password='testpassword')

        response = self.client.get(reverse('user', args=['1']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
