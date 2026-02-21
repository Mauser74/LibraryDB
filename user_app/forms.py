from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from user_app.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации нового пользователя"""
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите e-mail'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'date_of_birth',)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        user_model = get_user_model()
        if user_model.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже зарегистрирован')
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите e-mail'}),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        return username

