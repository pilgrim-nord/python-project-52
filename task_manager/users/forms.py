from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Константы — SonarCloud их не трогает
USERNAME_FIELD = 'username'
PASSWORD1_FIELD = 'password1'
PASSWORD2_FIELD = 'password2'


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Обязательное поле.'}
    )
    last_name = forms.CharField(
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Обязательное поле.'}
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", USERNAME_FIELD, PASSWORD1_FIELD, PASSWORD2_FIELD)
        labels = {
            USERNAME_FIELD: 'Имя пользователя',
            PASSWORD1_FIELD: 'Пароль',
            PASSWORD2_FIELD: 'Подтверждение пароля',
        }
        help_texts = {
            USERNAME_FIELD: 'Обязательное поле. Не более 150 символов. Только буквы, цифры и @/./+/-/_',
            PASSWORD1_FIELD: 'Ваш пароль должен содержать как минимум 3 символа.',
            PASSWORD2_FIELD: 'Для подтверждения введите пароль ещё раз.',
        }
        error_messages = {
            USERNAME_FIELD: {
                'required': 'Обязательное поле.',
                'unique': 'Пользователь с таким именем уже существует.',
                'max_length': 'Не более 150 символов.',
            },
            PASSWORD1_FIELD: {'required': 'Обязательное поле.'},
            PASSWORD2_FIELD: {'required': 'Обязательное поле.'},
        }
        # УБРАЛИ widgets отсюда — они больше не нужны
        # widgets = { ... }  ← удалить весь блок!

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Теперь безопасно обращаемся по константам
        self.fields[USERNAME_FIELD].help_text = (
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и символы @/./+/-/_.'
        )
        self.fields[PASSWORD1_FIELD].widget.attrs.update({
            'placeholder': 'Пароль',
            'class': 'form-control',
            'autocomplete': 'new-password',
        })
        self.fields[PASSWORD2_FIELD].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'new-password',
        })

    def clean_password2(self):
        p1 = self.cleaned_data.get(PASSWORD1_FIELD)
        p2 = self.cleaned_data.get(PASSWORD2_FIELD)
        if p1 and p2 and p1 != p2:
            raise ValidationError("Два поля пароля не совпадают.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'autocomplete': 'new-password'
        }),
        required=False,
        help_text='Оставьте пустым, если не хотите менять пароль.',
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password'
        }),
        required=False,
        help_text='Введите пароль ещё раз',
    )

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
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p1 != p2:
            raise ValidationError('Пароли не совпадают')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user