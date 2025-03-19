from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models.usuario import Usuario

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2')