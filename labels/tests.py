from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Label


class LabelListViewTest(TestCase):
    fixtures = ['users.json', 'labels.json']

    def test_list_requires_login(self):
        response = self.client.get(reverse('labels_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('labels_list')}")

    def test_list_authenticated(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bug')
        self.assertContains(response, 'feature')
        self.assertContains(response, 'documentation')


class LabelCreateViewTest(TestCase):
    fixtures = ['users.json']

    def test_create_requires_login(self):
        response = self.client.get(reverse('labels_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('labels_create')}")

    def test_create_valid_label(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(reverse('labels_create'), {'name': 'New label'})
        self.assertRedirects(response, reverse('labels_list'))
        self.assertTrue(Label.objects.filter(name='New label').exists())

    def test_create_duplicate_name_shows_error(self):
        Label.objects.create(name='Existing')
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(reverse('labels_create'), {'name': 'Existing'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.filter(name='Existing').count(), 1)


class LabelUpdateViewTest(TestCase):
    fixtures = ['users.json', 'labels.json']

    def test_update_requires_login(self):
        label = Label.objects.get(pk=1)
        response = self.client.get(reverse('labels_update', args=[label.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('labels_update', args=[label.pk])}")

    def test_update_valid_label(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        label = Label.objects.get(pk=1)
        response = self.client.post(reverse('labels_update', args=[label.pk]), {'name': 'Updated label'})
        self.assertRedirects(response, reverse('labels_list'))
        label.refresh_from_db()
        self.assertEqual(label.name, 'Updated label')


class LabelDeleteViewTest(TestCase):
    fixtures = ['users.json', 'labels.json']

    def test_delete_requires_login(self):
        label = Label.objects.get(pk=1)
        response = self.client.get(reverse('labels_delete', args=[label.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('labels_delete', args=[label.pk])}")

    def test_delete_label(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        label = Label.objects.get(pk=3)
        response = self.client.post(reverse('labels_delete', args=[label.pk]))
        self.assertRedirects(response, reverse('labels_list'))
        self.assertFalse(Label.objects.filter(pk=3).exists())


class LabelProtectionTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_cannot_delete_label_linked_to_task(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        label = Label.objects.get(pk=1)
        response = self.client.post(reverse('labels_delete', args=[label.pk]))
        self.assertRedirects(response, reverse('labels_list'))
        self.assertTrue(Label.objects.filter(pk=1).exists())
