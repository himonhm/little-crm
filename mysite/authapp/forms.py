from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from . import mixins


class CustomUserCreationForm(mixins.BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")


class CustomAuthenticationForm(mixins.BootstrapFormMixin, AuthenticationForm):
    pass
