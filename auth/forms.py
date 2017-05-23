from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

my_default_errors = {
    'required': 'Это поле обязятельно для заполнения',
    'invalid': 'Введите правильный формат',
    'unique': 'Пользователь с таким логином уже существует',
    'password_mismatch': 'Пароли не совпали',
    'mismatch': 'Неверный пароль',
    'password_too_short': 'Введите не менее 8ми символов'
}


# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    # User._meta.get_field('password2').verbose_name = 'подтвердить пароль'
    username = forms.CharField(label="Имя пользователя", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Пароль", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, help_text="Обязательное. До 150 символов.", label='Логин',
                               error_messages=my_default_errors)
    first_name = forms.CharField(max_length=30, required=False, help_text='Опционально.', label='Имя')
    last_name = forms.CharField(max_length=30, required=False, help_text='Опционально.', label='Фамилия')
    email = forms.EmailField(max_length=254, help_text='Обязательное для заполнения. Вводить действительный email',
                             error_messages=my_default_errors)
    password1 = forms.CharField(max_length=30, required=False, help_text='Обязательно. Не менее восьми символов',
                                label='Пароль', error_messages=my_default_errors, widget=forms.PasswordInput, )
    password2 = forms.CharField(max_length=30, required=False, help_text='Обязательно. Повторите пароль ',
                                label='Подтвердите пароль', error_messages=my_default_errors,
                                widget=forms.PasswordInput, )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
