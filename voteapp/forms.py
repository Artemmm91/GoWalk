from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from voteapp.models import Poll


class SignUpForm(UserCreationForm):
    username = forms.CharField(help_text='Только буквы, цифры и знаки @/./+/-/_', label='Логин')
    email = forms.EmailField(max_length=254, help_text='Введите корректную почту', label='Почта')
    password1 = forms.CharField(help_text='Сложный; как минимум 8 символов; не только из цифр', label='Пароль',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(help_text='Введите такой же пароль', label='Подтверждение пароля',
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class AddWalkForm(forms.Form):
    name = forms.CharField(label='Название маршрута', max_length=20)
    text = forms.CharField(label='Описание', max_length=400)
    link = forms.CharField(label='Ссылка Google Map', max_length=1000)


class AuthForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class SearchForm(forms.Form):
    check = forms.CharField(label="Поиск", max_length=100)


class RecoverForm(forms.Form):
    username = forms.CharField(label='Логин')


class CommentForm(forms.Form):
    text = forms.CharField(label="Ваш комментарий", max_length=400)
