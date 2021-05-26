from django.contrib import admin

from .models import PaymentSystem


@admin.register(PaymentSystem)
class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "title", "group")
    list_filter = ("group",)
