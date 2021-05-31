from django.dispatch import Signal

invoice_checking = Signal(providing_args=['payer', 'invoice'])
invoice_paid = Signal(providing_args=['payer', 'invoice'])