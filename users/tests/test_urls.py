from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import register_view, login_view, logout_view, user_view, update_user_view


class TestUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register_view)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_view)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_view)

    def test_user_profile_url_resolves(self):
        url = reverse('user', args=['1'])
        self.assertEquals(resolve(url).func, user_view)

    def test_update_user_profile_url_resolves(self):
        url = reverse('update-user')
        self.assertEquals(resolve(url).func, update_user_view)
