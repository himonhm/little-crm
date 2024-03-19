import json
from django.http import HttpRequest

from . import models
from . import forms


def change_suborder_status(request: HttpRequest):
    status_pk = request.POST.get("status_pk")
    suborder_pk = request.POST.get("suborder_pk")

    status, _ = models.Status.objects.get_or_create(pk=status_pk)
    suborder = models.SubOrder.objects.select_for_update().get(pk=suborder_pk)

    suborder.status = status
    is_ready = status.name in {"Shipped", "Ready"}

    for good in suborder.goods.select_for_update():
        good.is_ready = is_ready
        good.save(update_fields=["is_ready"])

    suborder.save(update_fields=["status"])
    suborder.order.update_order_status()


def get_dashboard_context_data():
    orders_queryset = models.Order.objects.exclude(status__name="Shipped")
    goods_queryset = models.Good.objects.filter(is_ready=False)
    statuses_queryset = models.Status.objects.all()

    return {
        "orders_not_done_count": orders_queryset.count(),
        "orders_not_done_last": orders_queryset.order_by(
            "status__ordering", "-created_at"
        )[:30],
        "goods_in_work": goods_queryset.count(),
        "statuses_all": statuses_queryset,
    }


def create_order_with_suborders(request: HttpRequest):
    json_data = request.POST.get("json")
    json_dict = json.loads(json_data) if json_data else {}

    order_form = forms.OrderForm(data=json_dict.get("order", {}))
    suborders_forms = [
        forms.SubOrderCreationForm(data=suborder)
        for suborder in json_dict.get("suborders", [])
    ]

    if not order_form.is_valid() or not all(
        form.is_valid() for form in suborders_forms
    ):
        return False

    order = order_form.save(commit=False)
    order.user = request.user
    order.status = models.Status.objects.get_or_create(name="Created")[0]
    order.save()

    for suborder_form in suborders_forms:
        suborder = suborder_form.save(commit=False)
        suborder.order = order
        suborder.user = request.user
        suborder.status = order.status
        suborder.save()
        amount_goods = int(suborder_form.data.get("amount", 0)) or 0
        for _ in range(amount_goods):
            models.Good.objects.create(sub_order=suborder, good_type=suborder.good_type)

    return True
