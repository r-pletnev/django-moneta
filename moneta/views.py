import json
import logging
from typing import Optional

from django.views.generic import FormView, View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from moneta import signals
from moneta.models import PaymentSystem, Invoice
from moneta.configuration import moneta_config, UrlGenerator
from moneta.schemas import CheckParameters

log = logging.getLogger("moneta-log")


def hook_view(request):
    log.debug(request.GET)
    return HttpResponse("SUCCESS")


class CheckNotificationView(View):
    """Handler checking notification from payment server"""

    @staticmethod
    def create_invoice(params: CheckParameters) -> Invoice:
        values = params.dict()
        values["test_mode"] = params.get_test_mode()
        values["status"] = Invoice.CHECK
        values["payment_system"] = params.get_payment_system()
        values["payment_system_unit_id"] = params.unit_id
        del values["command"]
        del values["moneta_user"]
        del values["unit_id"]
        return Invoice.objects.get_or_create(
            transaction_id=params.transaction_id, defaults=values
        )

    @staticmethod
    def xml_response(params: CheckParameters) -> str:
        """
        MONETA RESULT CODES:
            - 100: Answer contains amount field. This code should use when check query doen not contain MNT_AMONT
            - 200: Order paid. Notification about paid delivered.
            - 302: Order processing.
            - 402: Order created and ready to pay. Pay notification did not deliver
            - 500: Order outdated. Pay process will be ended.

            In normal cases merchant should return 402 or 100 codes
        """
        code = 402
        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <MNT_RESPONSE>
            <MNT_ID>{params.merchant_id}</MNT_ID>
            <MNT_TRANSACTION_ID>{params.transaction_id}</MNT_TRANSACTION_ID>
            <MNT_RESULT_CODE>{code}</MNT_RESULT_CODE>
        </MNT_RESPONSE>
                """

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf-8"))
        params = CheckParameters(**body)
        invoice = self.create_invoice(params)
        signals.invoice_checking.send(sender=self, invoice=invoice)
        return HttpResponse(self.xml_response(params), content_type="text/xml")

    def get(self, request):
        params = CheckParameters(**request.GET.dict())
        invoice = self.create_invoice(params)
        signals.invoice_checking.send(sender=self, invoice=invoice)
        return HttpResponse("YES")


class PaidNotificationView(View):
    """Handler notification that user paid payment"""

    pass


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
