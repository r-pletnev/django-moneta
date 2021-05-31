from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional

from moneta.models import PaymentSystem


class CheckParameters(BaseModel):
    """
    check parameters
     https://demo.moneta.ru/doc/MONETA.Assistant.ru.pdf
    """

    command: str = Field(alias="MNT_COMMAND")
    merchant_id: int = Field(alias="MNT_ID")
    transaction_id: str = Field(alias="MNT_TRANSACTION_ID")
    operation_id: Optional[str] = Field(alais="MNT_OPERATION_ID")
    amount: Optional[Decimal] = Field(alias="MNT_AMOUNT")
    currency: str = Field(alias="MNT_CURRENCY_CODE")
    subscriber_id: int = Field(alias="MNT_SUBSCRIBER_ID")
    test_mode: str = Field(alias="MNT_TEST_MODE")
    signature: str = Field(alias="MNT_SIGNATURE")
    moneta_user: Optional[str] = Field(alias="MNT_USER")
    unit_id: str = Field(alias="paymentSystem.unitId")
    corraccount: Optional[str] = Field(alias="MNT_CORRACCOUNT")

    def get_payment_system(self) -> Optional[PaymentSystem]:
        return PaymentSystem.objects.filter(unit_id=self.unit_id).last()

    def get_test_mode(self) -> bool:
        return bool(int(self.test_mode))
