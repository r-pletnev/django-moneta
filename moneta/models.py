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


class Invoice:
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    merchant_id = models.CharField(help_text="MNT_ID", max_length=30)
    transaction_id = models.CharField(max_length=20, unique=True)
    operation_id = models.CharField(max_length=30, help_text="MNT_OPERATION_ID")
    amount = models.DecimalField(
        max_digits=11, decimal_places=2, help_text="MNT_AMOUNT"
    )
    description = models.CharField(max_length=200)
    currency = models.CharField(max_length=3, help_text="MNT_CURRENCY_CODE")
    payment_system = models.ForeignKey("PaymentSystem", on_delete=models.SET_NULL)
    test_mode = models.BooleanField(help_text="MNT_TEST_MODE")
    signature = models.CharField(max_length=250, help_text="MNT_SIGNATURE")
    payment_system_unit_id = models.CharField(
        max_length=10, help_text="paymentSystem.unitId"
    )
    corraccount = models.CharField(max_length=20, help_text="MNT_CORRACCOUNT")

    class Meta:
        db_table = "mnt_invoices"
