from typing import Optional

from django.views.generic import FormView, View
from django.http import HttpResponse, HttpResponseRedirect
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from moneta.models import PaymentSystem
from moneta.configuration import moneta_config, UrlGenerator

log = logging.getLogger("moneta-log")


def hook_view(request):
    log.debug(request.GET)
    return HttpResponse("SUCCESS")


class CheckNotificationView(View):
    """Handler checking notification from payment server"""


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


class PaymentInitApiView(APIView, PaymentURLMixin):
    """
    EXAMPLE View for RESTfull apis.
    It generates url for PayAnyWay payment system.
    Documentation: https://demo.moneta.ru/doc/MONETA.Assistant.ru.pdf
    """

    def get(self, request, order_id, amount):
        url = self.get_payment_url(order_id=order_id, amount=amount)
        return Response({"payment_url": url})


class PaymentInitFormView(FormView, PaymentURLMixin):
    """
    EXAMPLE: Standart Form View.
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
