from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Status
# from task_manager.tasks.models import Task
from .forms import StatusForm

# Create your views here.


class StatusListView(ListView):
    model = Status
    template_name = 'status/list.html'
    context_object_name = 'statuses'