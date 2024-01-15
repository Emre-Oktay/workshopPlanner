from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils import timezone

from events.models import Event, Category, Location
from users.models import User

import time


class TestEventListPage(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = Options()
        service = Service(executable_path='functional_tests/chromedriver.exe')

        self.browser = webdriver.Chrome(
            service=service, options=chrome_options)

    def tearDown(self):
        self.browser.close()

    def test_events_button_redirects_to_event_list_page(self):
        self.browser.get(self.live_server_url)
        list_url = self.live_server_url + reverse('event_list')
        events_link = self.browser.find_element(By.LINK_TEXT, 'Events')
        events_link.click()
        self.assertEquals(self.browser.current_url, list_url)

    def test_no_events_is_displayed(self):
        self.browser.get(self.live_server_url)
        events_link = self.browser.find_element(By.LINK_TEXT, 'Events')
        events_link.click()
        alert = self.browser.find_element(
            By.XPATH, '//h5[text()="There are no events available"]')
        self.assertEquals(
            alert.text, 'There are no events available')

    def test_user_sees_events_list(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        location = Location.objects.create(
            user=user,
            city='Test City',
            district='Test District',
            street='Test Street',
            building_number='123',
            floor=1
        )
        category = Category.objects.create(
            name='Test Category'
        )
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date(),
            location=location,
            creator=user,
            category=category
        )
        self.browser.get(self.live_server_url)
        events_link = self.browser.find_element(By.LINK_TEXT, 'Events')
        events_link.click()
        event_title_element = self.browser.find_element(
            By.XPATH, '//h5[@class="card-title" and text()="Test Event"]')
        self.assertEquals(event_title_element.text, 'Test Event')

    def test_user_is_redirected_to_event_detail(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        location = Location.objects.create(
            user=user,
            city='Test City',
            district='Test District',
            street='Test Street',
            building_number='123',
            floor=1
        )
        category = Category.objects.create(
            name='Test Category'
        )
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date(),
            location=location,
            creator=user,
            category=category
        )
        self.browser.get(self.live_server_url)
        events_link = self.browser.find_element(By.LINK_TEXT, 'Events')
        events_link.click()
        event_detail_button = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/div/div[1]/div/div/div/a/div/button')
        self.browser.maximize_window()
        event_detail_button.click()
        detail_url = self.live_server_url + \
            reverse('event_detail', args=[event.id])
        self.assertEquals(self.browser.current_url, detail_url)
