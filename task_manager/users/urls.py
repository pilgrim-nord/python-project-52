from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
     path('', views.UserListView.as_view(), name='list'),

    # Регистрация нового пользователя
    path('create/', views.UserCreateView.as_view(), name='create'),

    # Редактирование пользователя
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='update'),

    # Удаление пользователя
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),

    path('', include('django.contrib.auth.urls')),
]