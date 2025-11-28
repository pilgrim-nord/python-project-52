
from django import forms

from .models import Task
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Querysets
        self.fields['executor'].queryset = User.objects.all()
        self.fields['status'].queryset = Status.objects.all()
        self.fields['labels'].queryset = Label.objects.all()
        # label для select по исполнителю
        self.fields['executor'].label_from_instance = (
            lambda obj: obj.get_full_name()
        )