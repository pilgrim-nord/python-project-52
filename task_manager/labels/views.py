# task_manager/labels/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


LABELS_LIST_URL = 'labels:list'


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy(LABELS_LIST_URL)

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно создана')
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy(LABELS_LIST_URL)

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно изменена')
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy(LABELS_LIST_URL)

    def form_valid(self, form):
        # Проверяем, связана ли метка с задачами
        if self.get_object().task_set.exists():
            messages.error(
                self.request,
                'Невозможно удалить метку, потому что она используется'
            )
            return redirect(self.success_url)

        messages.success(self.request, 'Метка успешно удалена')
        return super().form_valid(form)