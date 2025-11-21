# task_manager/views.py
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib import messages

# Этот View отвечает за статичную главную страницу (/)
class IndexView(TemplateView):
    template_name = 'index.html'
