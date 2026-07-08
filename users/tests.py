from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import UserRegistrationForm

TEST_PASSWORD = 'Str0ngPass!1'
TEST_LOGIN_PASSWORD = 'testpass123'


class UserListViewTest(TestCase):
    fixtures = ['users.json']

    def test_list_accessible_anonymously(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ivanov')
        self.assertContains(response, 'Petrov')

    def test_list_shows_all_users(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(len(response.context['users']), User.objects.count())


class UserCreateViewTest(TestCase):
    def test_get_create_page(self):
        response = self.client.get(reverse('users_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_valid_user_redirects_to_login(self):
        data = {
            'first_name': 'Sidor',
            'last_name': 'Sidorov',
            'username': 'sidorov',
            'password': TEST_PASSWORD,
            'password_confirmation': TEST_PASSWORD,
        }
        response = self.client.post(reverse('users_create'), data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='sidorov').exists())

    def test_create_duplicate_username_shows_error(self):
        User.objects.create_user(username='dup', password=TEST_PASSWORD)
        data = {
            'first_name': 'Dup',
            'last_name': 'Dup',
            'username': 'dup',
            'password': TEST_PASSWORD,
            'password_confirmation': TEST_PASSWORD,
        }
        response = self.client.post(reverse('users_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='dup').count() > 1)

    def test_password_mismatch(self):
        data = {
            'first_name': 'X',
            'last_name': 'Y',
            'username': 'xyuser',
            'password': TEST_PASSWORD,
            'password_confirmation': 'DifferentPass!1',
        }
        response = self.client.post(reverse('users_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='xyuser').exists())


class UserUpdateViewTest(TestCase):
    fixtures = ['users.json']

    def test_update_requires_login(self):
        user = User.objects.get(pk=1)
        response = self.client.get(reverse('users_update', args=[user.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('users_update', args=[user.pk])}")

    def test_update_self(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        data = {
            'first_name': 'IvanUpdated',
            'last_name': 'Ivanov',
            'username': 'ivanov',
            'password': '',
            'password_confirmation': '',
        }
        response = self.client.post(reverse('users_update', args=[user.pk]), data)
        self.assertRedirects(response, reverse('users_list'))
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'IvanUpdated')

    def test_update_other_user_forbidden(self):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        self.client.force_login(user1)
        response = self.client.get(reverse('users_update', args=[user2.pk]))
        self.assertRedirects(response, reverse('users_list'))


class UserDeleteViewTest(TestCase):
    fixtures = ['users.json']

    def test_delete_requires_login(self):
        user = User.objects.get(pk=1)
        response = self.client.get(reverse('users_delete', args=[user.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('users_delete', args=[user.pk])}")

    def test_delete_self(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(reverse('users_delete', args=[user.pk]))
        self.assertRedirects(response, reverse('users_list'))
        self.assertFalse(User.objects.filter(pk=1).exists())

    def test_delete_other_user_forbidden(self):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        self.client.force_login(user1)
        response = self.client.post(reverse('users_delete', args=[user2.pk]))
        self.assertRedirects(response, reverse('users_list'))
        self.assertTrue(User.objects.filter(pk=2).exists())


class AuthViewTest(TestCase):
    fixtures = ['users.json']

    def test_login_redirects_to_home(self):
        response = self.client.post(reverse('login'), {
            'username': 'ivanov',
            'password': TEST_LOGIN_PASSWORD,
        })
        self.assertRedirects(response, reverse('home'))

    def test_logout_redirects_to_home(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))


class UserRegistrationFormTest(TestCase):
    def test_form_fields_labels(self):
        form = UserRegistrationForm()
        self.assertEqual(form.fields['first_name'].label, 'Имя')
        self.assertEqual(form.fields['last_name'].label, 'Фамилия')
        self.assertEqual(form.fields['username'].label, 'Имя пользователя')
        self.assertEqual(form.fields['password'].label, 'Пароль')
        self.assertEqual(form.fields['password_confirmation'].label, 'Подтверждение пароля')
