from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

from . import forms as authapp_forms


class RegisterView(CreateView):
    form_class = authapp_forms.CustomUserCreationForm
    template_name = "authapp/register.html"
    success_url = reverse_lazy("ordersapp:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class CustomLoginView(LoginView):
    template_name = "authapp/login.html"
    form_class = authapp_forms.CustomAuthenticationForm
    redirect_authenticated_user = True
