from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
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


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = STATUSES_LIST_URL

    def form_valid(self, form):
        # Проверяем, используется ли статус в задачах
        if self.get_object().task_set.exists():
            messages.error(
                self.request,
                _('Невозможно удалить статус, потому что он используется')
            )
            return redirect(self.success_url)

        messages.success(self.request, _('Статус успешно удалён'))
        return super().form_valid(form)