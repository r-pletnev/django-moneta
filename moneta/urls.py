from django.urls import path

from .views import (
    PaymentInitFormView,
    hook_view,
    payment_success,
    PaymentInitApiView,
    PaidNotificationView,
    CheckNotificationView,
)
from .forms import PaymentForm

app_name = "moneta"

urlpatterns = [
    path("hook", hook_view, name="hook-view"),
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
        payment_success, name='payment-success',
    ),
    path(
        "api_init_pay/<int:order_id>/<int:amount>",
        PaymentInitApiView.as_view(),
        name="api-init",
    ),
]
