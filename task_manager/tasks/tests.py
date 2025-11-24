# tasks/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Task
from statuses.models import Status
from labels.models import Label


class TaskTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.status = Status.objects.create(name='New')
        self.label1 = Label.objects.create(name='Bug')
        self.label2 = Label.objects.create(name='Feature')

        self.task1 = Task.objects.create(
            name='Task 1',
            description='Description 1',
            author=self.user1,
            status=self.status
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Task 2',
            description='Description 2',
            author=self.user2,
            status=self.status
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')

    def test_task_detail_view_for_author(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('tasks:detail', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')

    def test_task_detail_view_for_anonymous(self):
        response = self.client.get(reverse('tasks:detail', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_create_task_by_logged_in_user(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('tasks:create'), {
            'name': 'New Task',
            'description': 'New description',
            'status': self.status.pk,
            'executor': self.user2.pk,
            'labels': [self.label1.pk, self.label2.pk]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task', author=self.user1).exists())

    def test_update_task_by_author(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('tasks:update', kwargs={'pk': self.task1.pk}), {
            'name': 'Updated Task 1',
            'description': self.task1.description,
            'status': self.status.pk,
            'executor': self.task1.executor.pk if self.task1.executor else '',
            'labels': [self.label1.pk]
        })
        self.task1.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task1.name, 'Updated Task 1')

    def test_update_task_by_non_author(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('tasks:update', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_delete_task_by_author(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('tasks:delete', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_delete_task_by_non_author(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('tasks:delete', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_protect_user_deletion_with_tasks(self):
        with self.assertRaises(IntegrityError):
            self.user1.delete()
        self.assertTrue(User.objects.filter(pk=self.user1.pk).exists())