from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    ordering = ['username'] # Сортируем по имени пользователя

# 2. GET /users/create/ — страница регистрации
# 3. POST /users/create/ — создание пользователя
class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:login') # После регистрации перенаправляем на страницу входа

# 4. GET /users/<int:pk>/update/ — страница редактирования
# 5. POST /users/<int:pk>/update/ — обновление пользователя
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list') # После обновления возвращаемся к списку пользователей

# 6. GET /users/<int:pk>/delete/ — страница удаления
# 7. POST /users/<int:pk>/delete/ — удаление пользователя
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list') # После удаления возвращаемся к списку