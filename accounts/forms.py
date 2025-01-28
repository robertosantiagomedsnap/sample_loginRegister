from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']  # Inclua apenas os campos definidos no modelo
