from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Diet, Order


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class OrderDietForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_date_from', 'order_date_to', 'address']
        widgets = {
            'order_date_from': forms.DateInput(attrs={'type': 'date'}),
            'order_date_to': forms.DateInput(attrs={'type': 'date'}),
        }


