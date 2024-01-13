from django.test import TestCase
from django.utils import timezone

from events import models
from users.models import User

from datetime import time


class TestModels(TestCase):

    def setUp(self):
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

    def test_location_model_str(self):
        self.assertEqual(str(self.location), 'Test City, Test District')

    def test_event_str(self):
        self.assertEqual(str(self.event), 'Test Event')

    def test_session_item_str(self):
        self.session_item = models.EventSessionItem.objects.create(event=self.event, start_time=time(
            10, 0), end_time=time(12, 0), title='Test Session', description='Test Description')

        self.assertEqual(str(self.session_item),
                         '10:00:00 - 12:00:00 - Test Session')

    def test_tag_str(self):
        self.assertEqual(str(self.tag), 'Test Tag')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_comment_str(self):
        self.comment = models.Comment.objects.create(
            event=self.event, user=self.user, text='Test text')

        self.assertEqual(str(self.comment), 'testuser - Test Event')
