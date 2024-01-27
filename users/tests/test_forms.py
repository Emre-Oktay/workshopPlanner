from django.test import TestCase
from django.contrib.auth import get_user_model
from users.forms import RegistrationForm, UpdateUserForm


class RegistrationFormTest(TestCase):

    def test_form_rendering(self):
        form = RegistrationForm()
        self.assertIn('class="form-control"', str(form))

    def test_form_valid_data(self):
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'user_type': 'participant',
        })

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'invalid-email',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'mismatchedpassword',
            'user_type': 'invalid_choice',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', str(form.errors))
        self.assertIn('The two password fields didn’t match.',
                      str(form.errors))
        self.assertIn('Select a valid choice.', str(form.errors))


class UpdateUserFormTest(TestCase):

    def test_form_rendering(self):
        user = get_user_model().objects.create_user(
            username='testuser', password='testpassword')
        form = UpdateUserForm(instance=user)
        self.assertIn('class="form-control"', str(form))

    def test_form_valid_data(self):
        user = get_user_model().objects.create_user(
            username='testuser', password='testpassword')
        form = UpdateUserForm(data={
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'birth_date': '2022-01-01',
            'bio': 'Updated bio.',
        }, instance=user)

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        user = get_user_model().objects.create_user(
            username='testuser', password='testpassword')
        form = UpdateUserForm(data={
            'username': 'updateduser',
            'email': 'invalid-email',
            'first_name': 'Updated',
            'last_name': 'User',
            'birth_date': 'invalid-date',
            'bio': 'Updated bio.',
        }, instance=user)

        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', str(form.errors))
        self.assertIn('Enter a valid date.', str(form.errors))
