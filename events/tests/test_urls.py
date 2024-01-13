from django.test import SimpleTestCase
from django.urls import reverse, resolve
from events import views


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, views.home)

    def test_list_url_resolves(self):
        url = reverse('event_list')
        self.assertEquals(resolve(url).func, views.event_list)

    def test_event_detail_url_resolves(self):
        url = reverse('event_detail', args=['1'])
        self.assertEquals(resolve(url).func, views.event_detail)
