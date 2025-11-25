from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm
from django.shortcuts import render
from django.http import HttpResponse

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

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')


def index(request):
    a = None
    a.hello() # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")