from django.http import HttpRequest

from . import models


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
