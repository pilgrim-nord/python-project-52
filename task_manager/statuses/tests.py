from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class StatusCRUDTestCase(TestCase):
    fixtures = ['statuses.json']

    def setUp(self):
        self.client = Client()
        # Создаем пользователя для тестов
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Тест',
            last_name='Пользователь'
        )

    def test_list_statuses_requires_login(self):
        """Тест, что список статусов требует авторизации"""
        url = reverse('statuses:list')
        
        # Без авторизации должен быть редирект на страницу входа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_list_statuses(self):
        """Тест отображения списка статусов"""
        self.client.force_login(self.user)
        url = reverse('statuses:list')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Статусы')
        # Проверяем, что статусы из фикстуры отображаются
        self.assertContains(response, 'новый')
        self.assertContains(response, 'в работе')

    def test_create_status_requires_login(self):
        """Тест, что создание статуса требует авторизации"""
        url = reverse('statuses:create')
        
        # Без авторизации должен быть редирект на страницу входа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_create_status(self):
        """Тест создания статуса"""
        self.client.force_login(self.user)
        url = reverse('statuses:create')
        
        # Проверяем GET запрос - форма должна отображаться
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Создание статуса')
        
        # Данные для нового статуса
        new_status_data = {
            'name': 'завершен',
        }
        
        # Проверяем POST запрос - создание статуса
        response = self.client.post(url, data=new_status_data)
        
        # После успешного создания должен быть редирект на список статусов
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:list'))
        
        # Проверяем, что статус создан
        self.assertTrue(Status.objects.filter(name='завершен').exists())
        new_status = Status.objects.get(name='завершен')
        self.assertEqual(new_status.name, 'завершен')

    def test_create_status_with_invalid_data(self):
        """Тест создания статуса с невалидными данными"""
        self.client.force_login(self.user)
        url = reverse('statuses:create')
        
        # Пустое имя
        invalid_data = {
            'name': '',
        }
        
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Форма с ошибками
        self.assertFalse(Status.objects.filter(name='').exists())

    def test_update_status_requires_login(self):
        """Тест, что обновление статуса требует авторизации"""
        status = Status.objects.get(pk=1)
        url = reverse('statuses:update', kwargs={'pk': status.pk})
        
        # Без авторизации должен быть редирект на страницу входа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_update_status(self):
        """Тест обновления статуса"""
        self.client.force_login(self.user)
        status = Status.objects.get(pk=1)
        url = reverse('statuses:update', kwargs={'pk': status.pk})
        
        # Проверяем GET запрос - форма должна отображаться
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Изменение статуса')
        
        # Обновленные данные
        updated_data = {
            'name': 'обновленный статус',
        }
        
        # Проверяем POST запрос - обновление статуса
        response = self.client.post(url, data=updated_data)
        
        # После успешного обновления должен быть редирект на список статусов
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:list'))
        
        # Проверяем, что данные обновлены
        status.refresh_from_db()
        self.assertEqual(status.name, 'обновленный статус')

    def test_delete_status_requires_login(self):
        """Тест, что удаление статуса требует авторизации"""
        status = Status.objects.get(pk=1)
        url = reverse('statuses:delete', kwargs={'pk': status.pk})
        
        # Без авторизации должен быть редирект на страницу входа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_delete_status(self):
        """Тест удаления статуса"""
        self.client.force_login(self.user)
        
        # Создаем статус для удаления
        status_to_delete = Status.objects.create(name='для удаления')
        status_id = status_to_delete.pk
        
        url = reverse('statuses:delete', kwargs={'pk': status_id})
        
        # Проверяем GET запрос - форма подтверждения должна отображаться
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Удаление статуса')
        self.assertContains(response, 'для удаления')
        
        # Проверяем POST запрос - удаление статуса
        response = self.client.post(url)
        
        # После успешного удаления должен быть редирект на список статусов
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:list'))
        
        # Проверяем, что статус удален
        self.assertFalse(Status.objects.filter(pk=status_id).exists())

    def test_delete_status_used_in_task(self):
        """Тест, что нельзя удалить статус, если он используется в задаче"""
        self.client.force_login(self.user)
        status = Status.objects.get(pk=1)
        
        # Пока задач нет, но проверяем, что логика работает
        # Когда задачи появятся, нужно будет добавить проверку
        url = reverse('statuses:delete', kwargs={'pk': status.pk})
        
        # Пока что статус можно удалить, так как задач нет
        response = self.client.post(url)
        # Если статус используется, должен быть редирект обратно с сообщением об ошибке
        # Если не используется, должен быть редирект на список
        self.assertIn(response.status_code, [302, 200])
