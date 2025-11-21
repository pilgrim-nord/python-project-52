# task_manager/views.py
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib import messages
from .models import Status

# Этот View отвечает за статичную главную страницу (/)
class IndexView(TemplateView):
    template_name = 'index.html'

# Этот View отвечает за динамический список статусов (/statuses/)
class StatusListView(ListView):
    model = Status
    template_name = 'statuses/index.html'

# Этот View отвечает за создание нового статуса (/statuses/create/)
class StatusCreateView(CreateView):
    model = Status
    template_name = 'statuses/create.html'
    fields = ['name']
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)