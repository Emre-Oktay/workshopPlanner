from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from events import models
from users.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.event_list_url = reverse('event_list')
        self.event_detail_url = reverse('event_detail', args=['1'])

        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.location = models.Location.objects.create(
            user=self.user,
            city='Test City',
            district='Test District',
            street='Test Street',
            building_number='123',
            floor=1
        )
        self.category = models.Category.objects.create(
            name='Test Category'
        )
        self.tag = models.Tag.objects.create(name='Test Tag')
        self.event = models.Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date(),
            location=self.location,
            creator=self.user,
            category=self.category
        )

    def test_event_list_GET(self):
        response = self.client.get(self.event_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_list.html')

    def test_event_detail_GET(self):
        response = self.client.get(self.event_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_detail.html')

    def test_event_detail_POST_adds_new_comment(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            self.event_detail_url, {'comment': 'Test text'})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.event.comment_set.first().text, 'Test text')

    def test_event_detail_POST_no_data(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            self.event_detail_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.event.comment_set.count(), 0)

    def test_event_create_POST(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('create_event')

        response = self.client.post(url, {
            'title': 'Test Event 2',
            'description': 'Test Description',
            'date': timezone.now().date(),
            'location': self.location.id,
            'category': self.category.id,
            'new_tags': 'Test,tags'
        })

        event2 = models.Event.objects.latest('id')
        self.assertEquals(event2.title, 'Test Event 2')
