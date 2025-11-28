from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .filters import TaskFilter
from .models import Task
from .forms import TaskForm
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User


# class TaskListView(ListView):
#     model = Task
#     template_name = 'tasks/list.html'
#     context_object_name = 'tasks'
#     paginate_by = 10
#
#     # НОВЫЙ МЕТОД: Фильтрация queryset'а
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#         status_id = self.request.GET.get('status')
#         if status_id:
#             queryset = queryset.filter(status_id=status_id)
#
#         executor_id = self.request.GET.get('executor')
#         if executor_id:
#             queryset = queryset.filter(executor_id=executor_id)
#
#         label_id = self.request.GET.get('label')
#         if label_id:
#             queryset = queryset.filter(labels__id=label_id)
#
#         if self.request.GET.get('self_tasks') == 'on':
#             queryset = queryset.filter(author=self.request.user)
#
#         return queryset.distinct()
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context['status_filter'] = self.request.GET.get('status', '')
#         context['executor_filter'] = self.request.GET.get('executor', '')
#         context['label_filter'] = self.request.GET.get('label', '')
#         context['is_self_tasks'] = self.request.GET.get('self_tasks') == 'on'
#
#         context['statuses'] = Status.objects.all()
#         context['executors'] = User.objects.all()
#         context['labels'] = Label.objects.all()
#
#         return context
class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = Label.objects.all()
        
        # Передача выбранных значений фильтров
        context['status_filter'] = self.request.GET.get('status', '')
        context['executor_filter'] = self.request.GET.get('executor', '')
        context['label_filter'] = self.request.GET.get('label', '')
        context['is_self_tasks'] = self.request.GET.get('own_task') == 'on'
        
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author
    
    def handle_no_permission(self):
        from django.contrib import messages
        from django.http import HttpResponseRedirect
        
        messages.error(
            self.request, 
            "Задачу может удалить только ее автор"
        )
        # Перенаправляем на список задач вместо поднятия исключения
        return HttpResponseRedirect(reverse_lazy('tasks:list'))
    
    def form_valid(self, form):
        messages.success(self.request, "Задача успешно удалена")
        return super().form_valid(form)