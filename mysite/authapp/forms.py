from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    widget_attrs = {"class": "form-control", "id": "floatingText"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["username", "password1", "password2", "email"]:
            self.fields[field_name].widget.attrs.update(self.widget_attrs)

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")
