from django.urls import path
from . import views
from ..views import CustomLoginView

app_name = 'users'
urlpatterns = [
     path('', views.UserListView.as_view(), name='list'),

    # Регистрация нового пользователя
    path('create/', views.UserCreateView.as_view(), name='create'),

    # Редактирование пользователя
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='update'),

    # Удаление пользователя
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
    path(
        "login/",
        CustomLoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login"
    ),

    # path('', include('django.contrib.auth.urls')),
]