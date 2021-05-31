from decimal import Decimal

import pytest

from moneta.schemas import MonetaQueryParameters


def test_make_check_params():
    get_kwargs = {
        "MNT_COMMAND": "CHECK",
        "MNT_ID": "1",
        "MNT_TRANSACTION_ID": "1",
        "MNT_OPERATION_ID": "123",
        "MNT_AMOUNT": "1.24",
        "MNT_CURRENCY_CODE": "RUB",
        "MNT_SUBSCRIBER_ID": "1",
        "MNT_TEST_MODE": "0",
        "MNT_SIGNATURE": "sign",
        "paymentSystem.unitId": "43674",
        "MNT_CORRACCOUNT": "317",
    }
    params = MonetaQueryParameters(**get_kwargs)
    assert params.merchant_id == 1
    assert params.unit_id == "43674"
    assert params.amount == Decimal("1.24")
