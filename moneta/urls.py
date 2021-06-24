from django.urls import path

from .views import (
    PaymentInitFormView,
    SuccessView,
    FailView,
    PaymentInitApiView,
    PaidNotificationView,
    CheckNotificationView,
)
from .forms import PaymentForm

app_name = "moneta"

urlpatterns = [
    path(
        "check_notification",
        CheckNotificationView.as_view(),
        name="check-notification",
    ),
    path("paid_notification", PaidNotificationView.as_view(), name="paid-notification"),
    path(
        "init_pay",
        PaymentInitFormView.as_view(
            form_class=PaymentForm,
            template_name="moneta/init.html",
        ),
        name="init",
    ),
    path(
        "success",
        SuccessView.as_view(template_name='moneta/success.html'),
        name="payment-success",
    ),
    path(
        "fail",
        FailView.as_view(template_name='moneta/fail.html'),
        name="payment-fail",
    ),
    path(
        "api_init_pay/<int:order_id>/<int:amount>",
        PaymentInitApiView.as_view(),
        name="api-init",
    ),
]
