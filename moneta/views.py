import json
import logging
from typing import Optional

from django.views.generic import FormView, View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from moneta import signals
from moneta.models import PaymentSystem, Invoice
from moneta.configuration import moneta_config, UrlGenerator
from moneta.schemas import MonetaQueryParameters

log = logging.getLogger("moneta-log")


class SuccessView(TemplateView):

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FailView(TemplateView):

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CheckNotificationView(View):
    """Handler checking notification from payment server"""

    @staticmethod
    def create_invoice(params: MonetaQueryParameters) -> Invoice:
        values = params.dict()
        values["test_mode"] = params.get_test_mode()
        values["payment_system"] = params.get_payment_system()
        values["payment_system_unit_id"] = params.unit_id if params.unit_id else ""
        values["subscriber_id"] = params.subscriber_id if params.subscriber_id else ""
        del values["moneta_user"]
        del values["unit_id"]
        return Invoice.objects.create_check_invoice(
            transaction_id=params.transaction_id, values=values
        )

    def handle_input_data(self, input_data: dict) -> MonetaQueryParameters:
        params = MonetaQueryParameters(**input_data)
        invoice = self.create_invoice(params)
        signals.invoice_checking.send(sender=self, invoice=invoice)
        return params

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf-8"))
        params = self.handle_input_data(input_data=body)
        return HttpResponse(params.xml_body(), content_type="text/xml")

    def get(self, request):
        params = self.handle_input_data(input_data=request.GET.dict())
        return HttpResponse(params.xml_body(), content_type="text/xml")


class PaidNotificationView(View):
    """Handler notification that user paid payment"""

    @staticmethod
    def finalize_invoice(params: MonetaQueryParameters) -> Optional[Invoice]:
        return Invoice.objects.finalize(transaction_id=params.transaction_id)

    def get(self, request):
        params = MonetaQueryParameters(**request.GET.dict())
        invoice = self.finalize_invoice(params)
        if invoice is None:
            return HttpResponse("FAIL")
        signals.invoice_paid.send(sender=self, invoice=invoice)
        return HttpResponse("SUCCESS")


class PaymentURLMixin:
    @staticmethod
    def init_url_generator() -> UrlGenerator:
        return moneta_config.url_generator()

    def get_payment_url(
        self, order_id: str, amount: int, payment_system: Optional[PaymentSystem] = None
    ) -> str:
        url_generator = self.init_url_generator()

        return url_generator.payment_url(
            payment_system=payment_system, order_id=order_id, amount=amount
        )


class PaymentInitApiView(View, PaymentURLMixin):
    """
    EXAMPLE View for RESTfull apis.
    It generates url for PayAnyWay payment system.
    Documentation: https://demo.moneta.ru/doc/MONETA.Assistant.ru.pdf
    """

    def get(self, request, order_id, amount):
        url = self.get_payment_url(order_id=order_id, amount=amount)
        return JsonResponse({"payment_url": url})


class PaymentInitFormView(FormView, PaymentURLMixin):
    """
    EXAMPLE: Standard Form View.
    It redirects user to PayAnyWay url payment system
    Documentation: https://demo.moneta.ru/doc/MONETA.Assistant.ru.pdf
    """

    def form_valid(self, form):
        url = self.get_payment_url(
            order_id=form.cleaned_data.get("transaction_id"),
            amount=form.cleaned_data.get("amount"),
            payment_system=form.cleaned_data.get("payment_system"),
        )
        return HttpResponseRedirect(url)
