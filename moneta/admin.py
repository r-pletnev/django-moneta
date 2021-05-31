from django.contrib import admin

from .models import PaymentSystem, Invoice


@admin.register(PaymentSystem)
class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "title", "group")
    list_filter = ("group",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "transaction_id",
        "created",
        "status",
        "amount",
        "currency",
        "test_mode",
    )
