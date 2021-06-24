import pytest
from pydantic import ValidationError
from moneta.models import PaymentSystem
from moneta.configuration import UrlGenerator, QueryPayload, moneta_config


pytestmark = pytest.mark.django_db


def test_incorrect_init_url_generator():
    with pytest.raises(ValidationError):
        UrlGenerator()


def test_correct_init_url_generator():
    config = moneta_config.config()
    gen = UrlGenerator(config=config)


def test_root_url():
    config = moneta_config.config()
    gen = UrlGenerator(config=config)
    assert gen.root_url == "https://demo.moneta.ru/assistant.htm"


def test_signature():
    config = moneta_config.config()
    old_code = config.basic_config.account_code
    config.basic_config.account_code = 1
    gen = UrlGenerator(config=config)
    assert gen.signature(order_id=123, amount=10, subscriber_id="") == "58772071f3af102aef274797b8662029"
    config.basic_config.account_code = None
    assert gen.signature(order_id=12, amount=10, subscriber_id="") is None
    config.basic_config.account_code = old_code


def test_query_payload():
    query = {
        "account_id": "123",
        "transaction_id": "199",
        "amount": "10",
        "currency": "RUB",
        "test_mode": "1",
        "unit_id": "1",
        "limit_ids": "1",
        "signature": "sign",
    }

    result_query = {
        "MNT_ID": "123",
        "MNT_TRANSACTION_ID": "199",
        "MNT_AMOUNT": "10",
        "MNT_CURRENCY_CODE": "RUB",
        "MNT_TEST_MODE": "1",
        "paymentSystem.unitId": "1",
        "paymentSystem.limitIds": "1",
        "MNT_SIGNATURE": "sign",
    }

    payload = QueryPayload(**query)
    assert result_query == payload.dict(by_alias=True, exclude_none=True)


def test_payment_url():
    gen = moneta_config.url_generator()
    order_id = 1
    amount = 23.123
    payment_system = PaymentSystem.objects.filter(name="plastic").last()
    url = gen.payment_url(
        payment_system=payment_system, order_id=order_id, amount=amount
    )
    check_url = "https://demo.moneta.ru/assistant.htm?MNT_ID=123&MNT_TRANSACTION_ID=1&MNT_AMOUNT=23.12&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=1&paymentSystem.unitId=card&paymentSystem.limitIds=card&MNT_SUBSCRIBER_ID=&MNT_SIGNATURE=3d76ae1753d62adee43e6d0f810c69d5"
    assert url == check_url
    url = gen.payment_url(order_id=order_id, amount=amount)
    assert url == check_url
