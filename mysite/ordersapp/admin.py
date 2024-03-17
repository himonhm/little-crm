from django.contrib import admin

from . import models


class StatusAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "ordering", "pk")


class GoodTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "pk")


class GoodAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "serial_number",
        "created_at",
        "user",
        "sub_order",
        "archived",
    )


class SerialNumberAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "good_type", "user", "created_at")


class SubOrderInline(admin.TabularInline):
    model = models.SubOrder
    classes = ["collapse"]


class GoodInline(admin.TabularInline):
    model = models.Good
    classes = ["collapse"]


class OrderAdmin(admin.ModelAdmin):
    inlines = (SubOrderInline,)
    fieldsets = [
        (None, {"fields": ("number", "date", "user", "status")}),
    ]


class SubOrderAdmin(admin.ModelAdmin):
    inlines = (GoodInline,)

    list_display = (
        "order",
        "good_type",
        "amount",
        "user",
        "created_at",
    )

    def amount(self, obj: models.SubOrder) -> int:
        return obj.goods.count()


admin.site.register(models.Status, StatusAdmin)
admin.site.register(models.GoodType, GoodTypeAdmin)
admin.site.register(models.Good, GoodAdmin)
admin.site.register(models.SerialNumber, SerialNumberAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.SubOrder, SubOrderAdmin)
