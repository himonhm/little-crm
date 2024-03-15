from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login

from .forms import UserCreationFormWithExtraFields


class RegisterView(CreateView):
    form_class = UserCreationFormWithExtraFields
    template_name = "authapp/register.html"
    success_url = reverse_lazy("admin")

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
