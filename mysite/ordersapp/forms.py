from django.forms import ModelForm
from . import models


class OrderForm(ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        exclude = ["user", "created_at"]


class SubOrderCreationForm(ModelForm):
    class Meta:
        model = models.SubOrder
        fields = "__all__"
        exclude = ["user", "order", "shipping_date", "created_at"]
