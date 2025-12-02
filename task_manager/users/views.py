from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserRegistrationForm, UserUpdateForm

LOGIN_REQUIRED_MESSAGE = "Вы не авторизованы. Пожалуйста, выполните вход."
USERS_LIST_URL = 'users:list'


class AuthRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            LOGIN_REQUIRED_MESSAGE
        )
        return redirect('login')


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    ordering = ['username']


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован"

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            self.success_message
        )

        if not self.request.session.session_key:
            self.request.session.create()

        return response


class UserUpdateView(AuthRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy(USERS_LIST_URL)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                LOGIN_REQUIRED_MESSAGE
            )
            return redirect('login')

        if request.user.pk != int(kwargs.get('pk', 0)):
            messages.error(
                request,
                "У вас нет прав для изменения другого пользователя."
            )
            return redirect(USERS_LIST_URL)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)


class UserDeleteView(AuthRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy(USERS_LIST_URL)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                LOGIN_REQUIRED_MESSAGE
            )
            return redirect('login')

        user_to_delete = self.get_object()

        # Проверяем, что пользователь удаляет только себя
        if request.user.pk != user_to_delete.pk:
            messages.error(
                request,
                "У вас нет прав для изменения другого пользователя."
            )
            return redirect(USERS_LIST_URL)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_to_delete = self.get_object()

        # Проверяем, используется ли пользователь в задачах
        from task_manager.tasks.models import Task

        tasks_as_author = Task.objects.filter(author=user_to_delete).exists()
        tasks_as_executor = Task.objects.filter(
            executor=user_to_delete
        ).exists()

        if tasks_as_author or tasks_as_executor:
            messages.error(
                request,
                "Невозможно удалить пользователя, потому что он используется"
            )
            return redirect(USERS_LIST_URL)

        logout(self.request)
        super().post(request, *args, **kwargs)
        messages.success(request, "Пользователь успешно удален")
        return redirect(USERS_LIST_URL)