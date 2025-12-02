# task_manager/labels/tests.py

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone  # Импортируем для работы с датой
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

from .models import Label


class LabelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.label = Label.objects.create(name='Test Label')
        self.status = Status.objects.create(name='New Status')

    def test_label_list_view_shows_creation_date(self):
        """Тест, что список меток отображает дату создания."""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что дата создания метки присутствует на странице
        self.assertContains(
            response, self.label.created_at.strftime('%d.%m.%Y')
        )

    def test_label_create_sets_creation_date(self):
        """Тест, что при создании метки автоматически устанавливается дата."""
        self.client.login(username='testuser', password='password')
        # Запоминаем время перед созданием
        before_creation = timezone.now()

        self.client.post(reverse('labels:create'), {'name': 'New Label'})

        new_label = Label.objects.get(name='New Label')
        # Проверяем, что дата создания установлена и находится в нужном
        # диапазоне
        self.assertIsNotNone(new_label.created_at)
        self.assertTrue(
            before_creation <= new_label.created_at <= timezone.now()
        )

    # Остальные тесты остаются без изменений, так как логика не поменялась
    def test_label_update_view(self):
        self.client.login(username='testuser', password='password')
        resp = self.client.post(reverse('labels:update',
                                        kwargs={'pk': self.label.pk}),
                                {'name': 'Updated Label'})
        self.assertEqual(resp.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_delete_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('labels:delete',
                                            kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_failure_when_in_use(self):
        self.client.login(username='testuser', password='password')
        Task.objects.create(
            name='Test Task',
            description='Test Description',
            author=self.user,
            status=self.status
        ).labels.add(self.label)

        response = self.client.post(reverse('labels:delete',
                                            kwargs={'pk': self.label.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())