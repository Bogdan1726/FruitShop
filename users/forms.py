from django import forms
from django.contrib.auth.forms import UsernameField


class UserLoginForm(forms.Form):
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': False, 'class': 'form-control', 'placeholder': 'Username'}))

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control', 'placeholder': 'Пароль'}),
    )
