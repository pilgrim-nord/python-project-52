import django_filters
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


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
        field_name='labels',  # ← вот это главное!
        queryset=Label.objects.all(),
        label="Метка",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    own_task = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        method='own_tasks_filter',
        widget=forms.CheckboxInput()
    )

    def own_tasks_filter(self, queryset, name, value):
        """
        Фильтрует задачи,
        принадлежащие текущему пользователю (если value == True).
        """
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    def labels_filter(self, queryset, name, value):
        """
        Фильтрует задачи, содержащие ВСЕ выбранные метки (логика "И").
        Если выбраны метки [A, B], показываются только задачи, 
        которые одновременно содержат метки A И B.
        """
        if value:
            # Получаем список ID выбранных меток
            label_ids = [label.id for label in value]
            
            # Начинаем с пустого набора
            result_queryset = queryset.model.objects.none()
            
            # Для каждой выбранной метки фильтруем задачи
            # и объединяем результаты через UNION
            for label_id in label_ids:
                tasks_with_label = queryset.filter(labels__id=label_id)
                result_queryset = result_queryset.union(tasks_with_label, all=False)
            
            # Возвращаем задачи, которые содержат все выбранные метки
            return result_queryset.distinct()
        
        return queryset
    
    @property
    def qs(self):
        """
        Возвращает отфильтрованный queryset с distinct() для предотвращения дублирования
        при фильтрации по ManyToMany полям (метки).
        """
        return super().qs.distinct()

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'own_task']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['executor'].field.label_from_instance = (
            lambda obj: obj.get_full_name()
        )

