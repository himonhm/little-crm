from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from . import views


app_name = "authapp"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("authapp:login")),
        name="logout",
    ),
    # TODO Logout view
]
