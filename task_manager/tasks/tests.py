# tasks/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskTests(TestCase):
    def setUp(self):
        """Создаем пользователей, статусы, метки и задачи для тестов."""
        self.user1 = User.objects.create_user(
            username='user1', password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='password123'
        )

        self.status1 = Status.objects.create(name='Status 1')
        self.status2 = Status.objects.create(name='Status 2')

        self.label1 = Label.objects.create(name='Label 1')
        self.label2 = Label.objects.create(name='Label 2')

        # Создаем задачи с разными параметрами для проверки фильтров
        self.task1 = Task.objects.create(
            name='Task 1 (User1, Status1, Label1)',
            description='Description 1',
            author=self.user1,
            executor=self.user2,
            status=self.status1
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Task 2 (User1, Status2, Label2)',
            description='Description 2',
            author=self.user1,
            executor=self.user1,
            status=self.status2
        )
        self.task2.labels.add(self.label2)

        self.task3 = Task.objects.create(
            name='Task 3 (User2, Status1, Both Labels)',
            description='Description 3',
            author=self.user2,
            executor=self.user1,
            status=self.status1
        )
        self.task3.labels.add(self.label1, self.label2)

    # --- Существующие CRUD тесты ---
    def test_task_list_view_status_code(self):
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)

    # ... (остальные CRUD тесты остаются без изменений) ...
    def test_protect_user_deletion_with_tasks(self):
        with self.assertRaises(IntegrityError):
            self.user1.delete()
        self.assertTrue(User.objects.filter(pk=self.user1.pk).exists())

    # --- НОВЫЕ ТЕСТЫ ДЛЯ ФИЛЬТРАЦИИ ---

    def _get_task_ids_from_response(self, response):
        """Вспомогательный метод для получения ID задач из ответа."""
        return list(response.context['tasks'].values_list('id', flat=True))

    def test_filter_by_status(self):
        """Тест фильтрации по статусу."""
        self.client.login(username='user1', password='password123')
        response = self.client.get(
            reverse('tasks:list'), {'status': self.status2.pk}
        )

        self.assertEqual(response.status_code, 200)
        # Ожидаем, что останется только task2
        self.assertCountEqual(
            self._get_task_ids_from_response(response), [self.task2.pk]
        )

    def test_filter_by_executor(self):
        """Тест фильтрации по исполнителю."""
        self.client.login(username='user1', password='password123')
        response = self.client.get(
            reverse('tasks:list'), {'executor': self.user1.pk}
        )

        self.assertEqual(response.status_code, 200)
        # Ожидаем task2 и task3
        self.assertCountEqual(
            self._get_task_ids_from_response(response),
            [self.task2.pk, self.task3.pk]
        )

    def test_filter_by_label(self):
        """Тест фильтрации по метке."""
        self.client.login(username='user1', password='password123')
        response = self.client.get(
            reverse('tasks:list'), {'label': self.label1.pk}
        )

        self.assertEqual(response.status_code, 200)
        # Ожидаем task1 и task3
        self.assertCountEqual(
            self._get_task_ids_from_response(response),
            [self.task1.pk, self.task3.pk]
        )

    def test_filter_by_self_tasks(self):
        """Тест фильтрации 'Только свои задачи'."""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('tasks:list'), {'self_tasks': 'on'})

        self.assertEqual(response.status_code, 200)
        # Ожидаем task1 и task2, т.к. их автор - user1
        self.assertCountEqual(
            self._get_task_ids_from_response(response),
            [self.task1.pk, self.task2.pk]
        )

    def test_no_filter_shows_all_tasks(self):
        """Тест, что без фильтров показываются все задачи."""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('tasks:list'))

        self.assertEqual(response.status_code, 200)
        # Ожидаем все три задачи
        self.assertCountEqual(self._get_task_ids_from_response(response),
                              [self.task1.pk, self.task2.pk, self.task3.pk])

    def test_combined_filters(self):
        """Тест комбинации фильтров (статус и исполнитель)."""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('tasks:list'), {
            'status': self.status1.pk,
            'executor': self.user1.pk
        })

        self.assertEqual(response.status_code, 200)
        # Ожидаем только task3 (у нее Status1 и исполнитель user1)
        self.assertCountEqual(
            self._get_task_ids_from_response(response), [self.task3.pk]
        )