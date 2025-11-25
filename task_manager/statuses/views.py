from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Status
from .forms import StatusForm

STATUSES_LIST_URL = reverse_lazy('statuses:list')


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = STATUSES_LIST_URL
    success_message = _('Статус успешно создан')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = STATUSES_LIST_URL
    success_message = _('Статус успешно изменён')


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = STATUSES_LIST_URL
    success_message = _('Статус успешно удалён')

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        # Проверяем, используется ли статус в задачах
        # Пока задач нет, но подготовим проверку
        try:
            # Попытка импортировать Task, если приложение существует
            from task_manager.tasks.models import Task
            if Task.objects.filter(status=status).exists():
                messages.error(
                    request,
                    _('Невозможно удалить статус, потому что он используется')
                )
                return self.get(request, *args, **kwargs)
        except ImportError:
            # Если модель Task еще не существует, просто удаляем
            pass
        
        return super().post(request, *args, **kwargs)