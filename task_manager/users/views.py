from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    ordering = ['username']


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:login')

class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Вы не авторизованы. Пожалуйста, выполните вход.")
            return redirect('users:list')
        
        if request.user.pk != int(kwargs.get('pk', 0)):
            messages.error(request, "У вас нет прав для изменения другого пользователя.")
            return redirect('users:list')
        
        return super().dispatch(request, *args, **kwargs)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')

    def dispatch(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        
        # Проверяем, что пользователь удаляет только себя
        if request.user.pk != user_to_delete.pk:
            messages.error(request, "У вас нет прав для изменения другого пользователя.")
            return redirect('users:list')
        
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        
        # Проверяем, используется ли пользователь в задачах
        from task_manager.tasks.models import Task
        tasks_as_author = Task.objects.filter(author=user_to_delete).exists()
        tasks_as_executor = Task.objects.filter(executor=user_to_delete).exists()
        
        if tasks_as_author or tasks_as_executor:
            messages.error(request, "Невозможно удалить пользователя, потому что он используется")
            return redirect('users:list')
        
        return super().post(request, *args, **kwargs)


def index(request):
    a = None
    a.hello() # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")