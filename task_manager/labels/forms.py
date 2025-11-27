from django import forms
from .models import Label

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name'] # 'created_at' остается за кадром
        labels = {
            'name': 'Имя',
        }