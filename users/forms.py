from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Почта',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите логин или email'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль'
        })
    )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Пример: egor@gmail.com'})
    )

    telegram = forms.CharField(
        label='Telegram',
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Пример: @egor'})
    )

    class Meta:
        model = get_user_model()
        
        fields = ('username', 'email', 'telegram', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'telegram': 'Telegram_id'
        }
        help_texts = {
            'username': 'Может содержать буквы, цифры и символы @/./+/-/_',
            'telegram': 'Введите ваш Telegram username (начинается с @)',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Пример: Егор123'
            }),
        }

class ProfileEditForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ('email', 'telegram')
