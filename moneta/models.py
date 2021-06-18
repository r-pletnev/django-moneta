from typing import Optional
from django.db import models


class PaymentSystem(models.Model):
    ELECTRONIC = "electronic"
    BANK = "bank"
    GROUP_CHOICES = ((ELECTRONIC, ELECTRONIC), (BANK, BANK))

    group = models.CharField(max_length=10, choices=GROUP_CHOICES)
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    account_id = models.PositiveIntegerField()
    unit_id = models.CharField(max_length=100)
    create_invoice = models.BooleanField()

    def __str__(self) -> str:
        return f"PaymentSystem ({self.name})"

    class Meta:
        db_table = "mnt_payment_systems"


class InvoiceManager(models.Manager):
    def create_check_invoice(self, transaction_id: str, values: dict) -> "Invoice":
        return self.get_or_create(transaction_id=transaction_id, defaults=values)

    def finalize(self, transaction_id: str) -> Optional["Invoice"]:
        invoice = self.filter(transaction_id=transaction_id).last()
        if invoice is None:
            return None
        invoice.status = Invoice.PAID
        invoice.save(update_fields=["status"])
        return invoice


class Invoice(models.Model):
    CHECK = "CHECK"
    PAID = "PAID"
    status_choices = ((CHECK, CHECK), (PAID, PAID))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    merchant_id = models.CharField(help_text="MNT_ID", max_length=30)
    transaction_id = models.CharField(max_length=255, unique=True)
    operation_id = models.CharField(
        max_length=30, help_text="MNT_OPERATION_ID", blank=True, null=True
    )
    amount = models.DecimalField(
        max_digits=11, decimal_places=2, help_text="MNT_AMOUNT"
    )
    description = models.CharField(max_length=200, blank=True)
    currency = models.CharField(max_length=3, help_text="MNT_CURRENCY_CODE")
    payment_system = models.ForeignKey(
        "PaymentSystem", on_delete=models.SET_NULL, blank=True, null=True
    )
    test_mode = models.BooleanField(help_text="MNT_TEST_MODE")
    signature = models.CharField(max_length=250, help_text="MNT_SIGNATURE", blank=True)
    payment_system_unit_id = models.CharField(
        max_length=10, help_text="paymentSystem.unitId", blank=True
    )
    corraccount = models.CharField(
        max_length=20, help_text="MNT_CORRACCOUNT", blank=True, null=True
    )
    subscriber_id = models.CharField(
        help_text="MNT_SUBSCRIBER_ID", blank=True, max_length=200
    )
    status = models.CharField(max_length=6, choices=status_choices, default=CHECK)

    objects = InvoiceManager()

    def __str__(self) -> str:
        return f"Invoice ({self.id})"

    class Meta:
        db_table = "mnt_invoices"
