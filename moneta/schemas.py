from pydantic import BaseModel, Field
from typing import Optional


class CheckParameters(BaseModel):
    """
    check parameters
     https://demo.moneta.ru/doc/MONETA.Assistant.ru.pdf
    """

    command: str = Field(alias="MNT_COMMAND")
    account_id: str = Field(alias="MNT_ID")
    transaction_id: str = Field(alias="MNT_TRANSACTION_ID")
    operation_id: Optional[str] = Field(alais="MNT_OPERATION_ID")
    amount: Optional[str] = Field(alias="MNT_AMOUNT")
    currency: str = Field(alias="MNT_CURRENCY_CODE")
    subscriber_id: str = Field(alias="MNT_SUBSCRIBER_ID")
    test_mode: str = Field(alias="MNT_TEST_MODE")
    signature: str = Field(alias="MNT_SIGNATURE")
    moneta_user: Optional[str] = Field(alias="MNT_SIGNATURE")
    unit_id: str = Field(alias="paymentSystem.unitId")
    corr_account: Optional[str] = Field(alias="MNT_CORRACCOUNT")
