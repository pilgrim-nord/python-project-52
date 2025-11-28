import django_filters
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # labels = django_filters.ModelMultipleChoiceFilter(
    #     queryset=Label.objects.all(),
    #     label="Метка",
    #     widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
    #     method='labels_filter'
    # )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label="Метка",
        widget=forms.Select(attrs={'class': 'form-select'}),
        method='labels_filter'
    )

    self_tasks = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        method='own_tasks_filter',
        widget=forms.CheckboxInput()
    )

    def own_tasks_filter(self, queryset, name, value):
        """
        Фильтрует задачи,
        принадлежащие текущему пользователю (если value == True).
        """
        if value in [True, 'on', '1']:
            request = getattr(self, 'request', None)
            if (request and hasattr(request, 'user')
                    and request.user.is_authenticated):
                return queryset.filter(author=request.user)
        return queryset

    def labels_filter(self, queryset, name, value):
        """
        Фильтрует задачи по выбранной метке.
        """
        if value:
            return queryset.filter(labels__id=value.id)
        
        return queryset
    
    @property
    def qs(self):
        """
        Возвращает отфильтрованный queryset с distinct() для
        предотвращения дублирования при фильтрации по ManyToMany полям (метки).
        """
        return super().qs.distinct()

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['executor'].field.label_from_instance = (
            lambda obj: obj.get_full_name()
        )

