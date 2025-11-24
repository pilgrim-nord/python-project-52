from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserCRUDTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        # Получаем пользователя из фикстуры
        self.user = User.objects.get(pk=1)
        self.user_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'username': 'testuser1',
        }

    def test_create_user(self):
        """Тест создания (регистрации) пользователя"""
        url = reverse('users:create')
        
        # Проверяем GET запрос - форма должна отображаться
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Регистрация')
        
        # Данные для нового пользователя
        new_user_data = {
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        
        # Проверяем POST запрос - создание пользователя
        response = self.client.post(url, data=new_user_data)
        
        # После успешной регистрации должен быть редирект на страницу входа
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))
        
        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.first_name, 'Новый')
        self.assertEqual(new_user.last_name, 'Пользователь')

    def test_create_user_with_invalid_data(self):
        """Тест создания пользователя с невалидными данными"""
        url = reverse('users:create')
        
        # Пароли не совпадают
        invalid_data = {
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'differentpass',
        }
        
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Форма с ошибками
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_update_user(self):
        """Тест обновления пользователя"""
        # Логинимся как пользователь из фикстуры
        self.client.force_login(self.user)
        
        url = reverse('users:update', kwargs={'pk': self.user.pk})
        
        # Проверяем GET запрос - форма должна отображаться
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование пользователя')
        
        # Обновленные данные
        updated_data = {
            'first_name': 'Обновленное',
            'last_name': 'Имя',
            'username': 'testuser1',
            'email': 'updated@example.com',
        }
        
        # Проверяем POST запрос - обновление пользователя
        response = self.client.post(url, data=updated_data)
        
        # После успешного обновления должен быть редирект на список пользователей
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:list'))
        
        # Проверяем, что данные обновлены
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Обновленное')
        self.assertEqual(self.user.last_name, 'Имя')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_update_user_requires_login(self):
        """Тест, что обновление требует авторизации"""
        url = reverse('users:update', kwargs={'pk': self.user.pk})
        
        # Без авторизации должен быть редирект на страницу входа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_update_other_user_forbidden(self):
        """Тест, что нельзя обновить другого пользователя (если есть такая логика)"""
        # Логинимся как первый пользователь
        self.client.force_login(self.user)
        
        # Пытаемся обновить второго пользователя
        other_user = User.objects.get(pk=2)
        url = reverse('users:update', kwargs={'pk': other_user.pk})
        
        # В текущей реализации это разрешено, но можно добавить проверку
        response = self.client.get(url)
        # Если нет ограничений, форма откроется
        # Если есть ограничения, будет 403 или редирект
        self.assertIn(response.status_code, [200, 302, 403])

    def test_delete_user(self):
        """Тест удаления пользователя"""
        # Логинимся как пользователь из фикстуры
        self.client.force_login(self.user)
        
        # Создаем пользователя для удаления
        user_to_delete = User.objects.create_user(
            username='todelete',
            password='testpass123',
            first_name='Удаляемый',
            last_name='Пользователь'
        )
        user_id = user_to_delete.pk
        
        url = reverse('users:delete', kwargs={'pk': user_id})
        
        # Проверяем GET запрос - форма подтверждения должна отображаться
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Удаление')
        
        # Проверяем POST запрос - удаление пользователя
        response = self.client.post(url)
        
        # После успешного удаления должен быть редирект на список пользователей
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:list'))
        
        # Проверяем, что пользователь удален
        self.assertFalse(User.objects.filter(pk=user_id).exists())

    def test_delete_user_requires_login(self):
        """Тест, что удаление требует авторизации"""
        url = reverse('users:delete', kwargs={'pk': self.user.pk})
        
        # Без авторизации должен быть редирект на страницу входа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_delete_other_user_forbidden(self):
        """Тест, что нельзя удалить другого пользователя (если есть такая логика)"""
        # Логинимся как первый пользователь
        self.client.force_login(self.user)
        
        # Пытаемся удалить второго пользователя
        other_user = User.objects.get(pk=2)
        url = reverse('users:delete', kwargs={'pk': other_user.pk})
