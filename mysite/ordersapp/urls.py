from django.urls import path

from . import views


app_name = "ordersapp"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="index"),
    path("orders/", views.OrdersListView.as_view(), name="orders"),
]
