from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status

from .models import Task


class TaskListViewTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_list_requires_login(self):
        response = self.client.get(reverse('tasks_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('tasks_list')}")

    def test_list_authenticated(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fix login bug')
        self.assertContains(response, 'Add status filter')


class TaskDetailViewTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_detail_requires_login(self):
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('tasks_detail', args=[task.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('tasks_detail', args=[task.pk])}")

    def test_detail_authenticated(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('tasks_detail', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fix login bug')
        self.assertContains(response, 'Fix login bug')


class TaskCreateViewTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def test_create_requires_login(self):
        response = self.client.get(reverse('tasks_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('tasks_create')}")

    def test_create_valid_task_sets_author(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        status = Status.objects.get(pk=1)
        data = {
            'name': 'New task',
            'description': 'A new task description',
            'status': status.pk,
            'executor': user.pk,
        }
        response = self.client.post(reverse('tasks_create'), data)
        self.assertRedirects(response, reverse('tasks_list'))
        task = Task.objects.get(name='New task')
        self.assertEqual(task.author, user)

    def test_create_duplicate_name_shows_error(self):
        Task.objects.create(
            name='Existing task',
            status=Status.objects.get(pk=1),
            author=User.objects.get(pk=1),
        )
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        data = {
            'name': 'Existing task',
            'description': '',
            'status': Status.objects.get(pk=1).pk,
            'executor': user.pk,
        }
        response = self.client.post(reverse('tasks_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.filter(name='Existing task').count(), 1)


class TaskUpdateViewTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_update_requires_login(self):
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('tasks_update', args=[task.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('tasks_update', args=[task.pk])}")

    def test_update_valid_task(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        task = Task.objects.get(pk=1)
        data = {
            'name': 'Updated task name',
            'description': 'Updated description',
            'status': Status.objects.get(pk=2).pk,
            'executor': 2,
        }
        response = self.client.post(reverse('tasks_update', args=[task.pk]), data)
        self.assertRedirects(response, reverse('tasks_list'))
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated task name')


class TaskDeleteViewTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_delete_requires_login(self):
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('tasks_delete', args=[task.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('tasks_delete', args=[task.pk])}")

    def test_delete_by_non_author_forbidden(self):
        user2 = User.objects.get(pk=2)
        self.client.force_login(user2)
        task = Task.objects.get(pk=1)
        response = self.client.post(reverse('tasks_delete', args=[task.pk]))
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTrue(Task.objects.filter(pk=1).exists())

    def test_delete_by_author(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        task = Task.objects.get(pk=1)
        response = self.client.post(reverse('tasks_delete', args=[task.pk]))
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertFalse(Task.objects.filter(pk=1).exists())


class StatusProtectionTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_cannot_delete_status_linked_to_task(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        status = Status.objects.get(pk=2)
        response = self.client.post(reverse('statuses_delete', args=[status.pk]))
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTrue(Status.objects.filter(pk=2).exists())


class UserProtectionTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_cannot_delete_user_linked_to_task(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        response = self.client.post(reverse('users_delete', args=[user.pk]))
        self.assertRedirects(response, reverse('users_list'))
        self.assertTrue(User.objects.filter(pk=1).exists())


class TaskLabelsM2MTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_task_has_labels(self):
        task = Task.objects.get(pk=1)
        self.assertEqual(task.labels.count(), 1)
        self.assertTrue(task.labels.filter(name='bug').exists())

    def test_create_task_with_labels(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        status = Status.objects.get(pk=1)
        label1 = Label.objects.get(pk=1)
        label2 = Label.objects.get(pk=2)
        data = {
            'name': 'Task with labels',
            'description': 'Test M2M',
            'status': status.pk,
            'executor': user.pk,
            'labels': [label1.pk, label2.pk],
        }
        response = self.client.post(reverse('tasks_create'), data)
        self.assertRedirects(response, reverse('tasks_list'))
        task = Task.objects.get(name='Task with labels')
        self.assertEqual(task.labels.count(), 2)


class TaskFilterTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_filter_by_status(self):
        response = self.client.get(reverse('tasks_list'), {'status': 1})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        for task in tasks:
            self.assertEqual(task.status_id, 1)

    def test_filter_by_executor(self):
        response = self.client.get(reverse('tasks_list'), {'executor': 2})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        for task in tasks:
            self.assertEqual(task.executor_id, 2)

    def test_filter_by_label(self):
        response = self.client.get(reverse('tasks_list'), {'labels': 1})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        for task in tasks:
            self.assertTrue(task.labels.filter(pk=1).exists())

    def test_filter_self_tasks(self):
        response = self.client.get(reverse('tasks_list'), {'self_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        for task in tasks:
            self.assertEqual(task.author_id, self.user.pk)

    def test_filter_combined(self):
        response = self.client.get(reverse('tasks_list'), {'status': 2, 'executor': 2})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        for task in tasks:
            self.assertEqual(task.status_id, 2)
            self.assertEqual(task.executor_id, 2)

    def test_filter_empty_shows_all(self):
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), Task.objects.count())
