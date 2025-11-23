from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        error_messages={
            'required': 'Обязательное поле.',
        }
    )
    last_name = forms.CharField(
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        error_messages={
            'required': 'Обязательное поле.',
        }
    )
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        help_texts = {
            'username': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
            'password1': 'Ваш пароль должен содержать как минимум 3 символа.',
            'password2': 'Для подтверждения введите, пожалуйста, пароль ещё раз.',
        }
        error_messages = {
            'username': {
                'required': 'Обязательное поле.',
                'unique': 'Пользователь с таким именем уже существует.',
                'max_length': 'Убедитесь, что это значение содержит не более 150 символов.',
            },
            'password1': {
                'required': 'Обязательное поле.',
            },
            'password2': {
                'required': 'Обязательное поле.',
            },
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Два поля пароля не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UserUpdateForm(UserChangeForm):
    password = None  # Скрываем поле пароля

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Имя пользователя',
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя',
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Ваша фамилия',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control',
            }),
        }
