from django.test import TestCase
from django.utils import timezone

from events.forms import EventForm
from events import models
from users.models import User


class TestForms(TestCase):

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

    def test_event_form_valid_data(self):
        form = EventForm(data={
            'title': 'Test Event',
            'description': 'Test Description',
            'date': timezone.now().date(),
            'location': self.location.id,
            'category': self.category.id,
            'new_tags': 'Test,tags'
        })

        self.assertTrue(form.is_valid())

    def test_event_form_no_data(self):
        form = EventForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)
