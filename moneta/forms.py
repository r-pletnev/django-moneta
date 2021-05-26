from django import forms

from .models import PaymentSystem


class PaymentForm(forms.Form):
    transaction_id = forms.IntegerField(min_value=1)
    amount = forms.FloatField(min_value=1)
    payment_system = forms.ModelChoiceField(queryset=PaymentSystem.objects.all())
