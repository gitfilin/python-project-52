from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Status


class StatusListViewTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def test_list_requires_login(self):
        response = self.client.get(reverse('statuses_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('statuses_list')}")

    def test_list_authenticated(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Draft')
        self.assertContains(response, 'In progress')
        self.assertContains(response, 'Done')


class StatusCreateViewTest(TestCase):
    fixtures = ['users.json']

    def test_create_requires_login(self):
        response = self.client.get(reverse('statuses_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('statuses_create')}")

    def test_create_valid_status(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(reverse('statuses_create'), {'name': 'New status'})
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTrue(Status.objects.filter(name='New status').exists())

    def test_create_duplicate_name_shows_error(self):
        Status.objects.create(name='Existing')
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(reverse('statuses_create'), {'name': 'Existing'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.filter(name='Existing').count(), 1)


class StatusUpdateViewTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def test_update_requires_login(self):
        status = Status.objects.get(pk=1)
        response = self.client.get(reverse('statuses_update', args=[status.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('statuses_update', args=[status.pk])}")

    def test_update_valid_status(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        status = Status.objects.get(pk=1)
        response = self.client.post(reverse('statuses_update', args=[status.pk]), {'name': 'Updated name'})
        self.assertRedirects(response, reverse('statuses_list'))
        status.refresh_from_db()
        self.assertEqual(status.name, 'Updated name')


class StatusDeleteViewTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def test_delete_requires_login(self):
        status = Status.objects.get(pk=1)
        response = self.client.get(reverse('statuses_delete', args=[status.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('statuses_delete', args=[status.pk])}")

    def test_delete_status(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        status = Status.objects.get(pk=1)
        response = self.client.post(reverse('statuses_delete', args=[status.pk]))
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertFalse(Status.objects.filter(pk=1).exists())
