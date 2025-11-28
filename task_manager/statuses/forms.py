from django import forms

from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        labels = {
            'name': 'Имя',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }