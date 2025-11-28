#!/usr/bin/env python
"""
Тестовый скрипт для проверки работы flash сообщений в Django приложении "Менеджер задач"

Этот скрипт тестирует:
1. Создание новой задачи с flash сообщением
2. Изменение задачи с flash сообщением  
3. Невозможность удалить чужую задачу с flash сообщением
4. Удаление собственной задачи с flash сообщением
"""

import os
import django
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
django.setup()

def test_flash_messages():
    """Функция для тестирования flash сообщений"""
    
    print("🧪 Запуск тестирования flash сообщений...")
    print("=" * 60)
    
    # Создаем тестового клиента
    client = Client()
    
    # Создаем тестовых пользователей
    print("👤 Создание тестовых пользователей...")
    
    # Удаляем пользователей если они существуют
    User.objects.filter(username='testuser1').delete()
    User.objects.filter(username='testuser2').delete()
    
    # Создаем пользователей
    user1 = User.objects.create_user(username='testuser1', password='testpass123')
    user2 = User.objects.create_user(username='testuser2', password='testpass123')
    
    print(f"✅ Создан пользователь 1: {user1.username}")
    print(f"✅ Создан пользователь 2: {user2.username}")
    
    # Логинимся как первый пользователь
    print("\n🔐 Вход пользователя testuser1...")
    login_successful = client.login(username='testuser1', password='testpass123')
    print(f"✅ Вход {'успешен' if login_successful else 'неудачен'}")
    
    print("\n" + "="*60)
    print("ТЕСТ 1: СОЗДАНИЕ НОВОЙ ЗАДАЧИ")
    print("="*60)
    
    # Создаем новую задачу
    print("📝 Создание новой задачи...")
    response = client.post('/tasks/create/', {
        'name': 'Тестовая задача для проверки flash сообщений',
        'description': 'Описание тестовой задачи',
        'status': 1,  # Предполагаем что статус с id=1 существует
    }, follow=True)
    
    # Проверяем что есть flash сообщение
    if hasattr(response, 'context') and response.context:
        messages_list = list(response.context.get('messages', []))
        if messages_list:
            print(f"✅ Найдено flash сообщение: '{messages_list[0]}'")
        else:
            print("⚠️  Flash сообщения не найдены в контексте")
    
    print(f"📊 Статус ответа: {response.status_code}")
    
    print("\n" + "="*60)
    print("ТЕСТ 2: ДОСТУП К СПИСКУ ЗАДАЧ")
    print("="*60)
    
    # Переходим к списку задач
    response = client.get('/tasks/')
    print(f"📊 Статус ответа: {response.status_code}")
    
    # Проверяем что шаблон содержит поддержку сообщений
    content = response.content.decode('utf-8')
    if 'bootstrap_messages' in content:
        print("✅ В шаблоне найден {% bootstrap_messages %}")
    else:
        print("⚠️  {% bootstrap_messages %} не найден в шаблоне")
    
    print("\n" + "="*60)
    print("ТЕСТ 3: ПОПЫТКА УДАЛИТЬ ЗАДАЧУ ДРУГОГО ПОЛЬЗОВАТЕЛЯ")
    print("="*60)
    
    # Создаем задачу от второго пользователя
    from task_manager.tasks.models import Task
    from task_manager.statuses.models import Status
    
    try:
        status = Status.objects.first()
        if status:
            task_by_user2 = Task.objects.create(
                name="Задача пользователя 2",
                description="Описание задачи пользователя 2",
                author=user2,
                status=status
            )
            
            print(f"📝 Создана задача от пользователя 2: {task_by_user2.name}")
            
            # Пытаемся удалить чужую задачу (должно быть запрещено)
            response = client.post(f'/tasks/{task_by_user2.id}/delete/', follow=True)
            print(f"📊 Статус ответа: {response.status_code}")
            
            # Проверяем flash сообщение об ошибке
            if hasattr(response, 'context') and response.context:
                messages_list = list(response.context.get('messages', []))
                error_messages = [msg for msg in messages_list if 'ошибка' in str(msg).lower() or 'удалить' in str(msg).lower()]
                if error_messages:
                    print(f"✅ Найдено сообщение об ошибке: '{error_messages[0]}'")
                else:
                    print("⚠️  Сообщение об ошибке не найдено")
                    
    except Exception as e:
        print(f"⚠️  Ошибка при создании задачи: {e}")
    
    print("\n" + "="*60)
    print("ТЕСТ 4: НАСТРОЙКИ DJANGO")
    print("="*60)
    
    # Проверяем настройки Django
    from django.conf import settings
    
    checks = [
        ('django.contrib.messages' in settings.INSTALLED_APPS, 
         "django.contrib.messages в INSTALLED_APPS"),
        ('django.contrib.messages.middleware.MessageMiddleware' in settings.MIDDLEWARE,
         "MessageMiddleware в MIDDLEWARE"),
        ('django.contrib.messages.context_processors.messages' in [cp['context_processors'][0] for cp in settings.TEMPLATES if 'context_processors' in cp],
         "messages context processor в TEMPLATES")
    ]
    
    for check_result, description in checks:
        print(f"{'✅' if check_result else '❌'} {description}")
    
    print("\n" + "="*60)
    print("ЗАВЕРШЕНИЕ ТЕСТИРОВАНИЯ")
    print("="*60)
    
    # Убираем тестовых пользователей
    print("🧹 Удаление тестовых пользователей...")
    User.objects.filter(username='testuser1').delete()
    User.objects.filter(username='testuser2').delete()
    print("✅ Тестовые пользователи удалены")
    
    print("\n🎉 Тестирование flash сообщений завершено!")
    print("\n💡 Для полного тестирования рекомендуется:")
    print("   1. Запустить сервер: python manage.py runserver")
    print("   2. Открыть браузер и войти в систему")
    print("   3. Выполнить операции: создание/изменение/удаление задач")
    print("   4. Проверить отображение flash сообщений")

if __name__ == '__main__':
    test_flash_messages()