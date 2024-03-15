from django.urls import path

from . import views


app_name = "authapp"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    # TODO Login view
    # TODO Logout view
]
