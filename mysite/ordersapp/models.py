from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class GoodType(models.Model):
    """Model to represent types of goods."""

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    manual_link = models.URLField(blank=True, null=True, verbose_name=_("Manual link"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="good_types",
        verbose_name=_("User"),
    )
    archived = models.BooleanField(default=False, verbose_name=_("Archived"))

    class Meta:
        verbose_name = _("Good Type")
        verbose_name_plural = _("Good Types")

    def __str__(self) -> str:
        """Return string representation of the GoodType."""
        return self.name


class Status(models.Model):
    """Model to represent status of an object."""

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    color = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Color code")
    )
    ordering = models.PositiveSmallIntegerField(default=0, verbose_name=_("Ordering"))

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")

    def __str__(self) -> str:
        """Return string representation of the Status."""
        return self.name


class Order(models.Model):
    number = models.CharField(
        blank=True, null=True, max_length=100, verbose_name=_("Order number")
    )
    date = models.DateTimeField(blank=True, null=True, verbose_name=_("Order date"))
    status = models.ForeignKey(
        to=Status,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Status"),
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("User"),
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    def update_order_status(self):
        """
        Update order status to common status of all related OrderDetail instances,
        if they share the same status; otherwise, reset the status.
        """
        status_names = {
            suborders.status.name
            for suborders in self.sub_orders.all()
            if suborders.status
        }
        if len(status_names) == 1:
            self.status = Status.objects.get_or_create(name=status_names.pop())[0]
        else:
            self.status = None
        self.save(update_fields=["status"])

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self) -> str:
        return f"{self.number}"


class SubOrder(models.Model):
    good_type = models.ForeignKey(
        GoodType,
        on_delete=models.PROTECT,
        related_name="sub_orders",
        verbose_name=_("Good type"),
    )
    note = models.TextField(blank=True, null=True, verbose_name=_("Note"))
    buyer = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Buyer")
    )
    client = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Client")
    )
    status = models.ForeignKey(
        Status,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Status"),
    )
    production_time = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Production time")
    )
    shipping_date = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Shipping date")
    )
    shipping_photos_link = models.URLField(
        blank=True, null=True, verbose_name=_("Shipping photos link")
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="sub_orders",
        verbose_name=_("Order"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("User"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Suborder")
        verbose_name_plural = _("Suborders")

    def __str__(self):
        return f"{self.pk}"


class SerialNumber(models.Model):
    good_type = models.ForeignKey(
        GoodType,
        on_delete=models.PROTECT,
        related_name="serial_numbers",
        verbose_name=_("Good type"),
    )
    serial_number = models.CharField(
        max_length=100, unique=True, verbose_name=_("Serial number")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="serial_numbers",
        verbose_name=_("User"),
    )

    class Meta:
        verbose_name = _("Serial Number")
        verbose_name_plural = _("Serial Numbers")

    def __str__(self):
        return f"{self.serial_number}"


class Good(models.Model):
    good_type = models.ForeignKey(
        GoodType,
        null=True,
        on_delete=models.PROTECT,
        related_name="goods",
        verbose_name=_("Type of good"),
    )
    sub_order = models.ForeignKey(
        SubOrder,
        on_delete=models.CASCADE,
        related_name="goods",
        verbose_name=_("Suborder"),
    )
    serial_number = models.OneToOneField(
        "SerialNumber",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Serial number"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, verbose_name=_("User")
    )
    is_ready = models.BooleanField(default=False, verbose_name=_("Is ready"))
    archived = models.BooleanField(default=False, verbose_name=_("Archived"))

    class Meta:
        verbose_name = _("Good")
        verbose_name_plural = _("Goods")

    def __str__(self):
        return f"{self.serial_number}"
