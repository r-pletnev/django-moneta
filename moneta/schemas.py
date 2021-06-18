from decimal import Decimal
from hashlib import md5

from pydantic import BaseModel, Field
from typing import Optional

from moneta.models import PaymentSystem
from moneta.configuration import moneta_config


class MonetaQueryParameters(BaseModel):
    """
    check parameters
     https://demo.moneta.ru/doc/MONETA.Assistant.ru.pdf
    """

    # command: str = Field(alias="MNT_COMMAND")
    merchant_id: int = Field(alias="MNT_ID")
    transaction_id: str = Field(alias="MNT_TRANSACTION_ID")
    currency: str = Field(alias="MNT_CURRENCY_CODE")
    test_mode: str = Field(alias="MNT_TEST_MODE")
    signature: str = Field(alias="MNT_SIGNATURE")
    subscriber_id: Optional[str] = Field(alias="MNT_SUBSCRIBER_ID", default=None)
    amount: Optional[Decimal] = Field(alias="MNT_AMOUNT")
    operation_id: Optional[str] = Field(alais="MNT_OPERATION_ID")
    moneta_user: Optional[str] = Field(alias="MNT_USER")
    unit_id: Optional[str] = Field(alias="paymentSystem.unitId", default=None)
    corraccount: Optional[str] = Field(alias="MNT_CORRACCOUNT")

    def get_payment_system(self) -> Optional[PaymentSystem]:
        return PaymentSystem.objects.filter(unit_id=self.unit_id).last()

    def get_test_mode(self) -> bool:
        return bool(int(self.test_mode))

    @staticmethod
    def result_code() -> int:
        """
        MONETA RESULT CODES:
            - 100: Answer contains amount field. This code should use when check query doen not contain MNT_AMONT
            - 200: Order paid. Notification about paid delivered.
            - 302: Order processing.
            - 402: Order created and ready to pay. Pay notification did not deliver
            - 500: Order outdated. Pay process will be ended.

            In normal cases merchant should return 402 or 100 codes
        """
        return 402

    def get_signature(self, account_code: Optional[str] = None) -> str:
        if account_code is None:
            account_code = moneta_config.get_account_code()
        chunks = [
            str(self.result_code()),
            str(self.merchant_id),
            str(self.transaction_id),
            account_code,
        ]
        sign = "".join(chunks)
        return md5(sign.encode("utf-8")).hexdigest()

    def xml_body(self, account_code: Optional[str] = None) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <MNT_RESPONSE>
            <MNT_ID>{self.merchant_id}</MNT_ID>
            <MNT_TRANSACTION_ID>{self.transaction_id}</MNT_TRANSACTION_ID>
            <MNT_RESULT_CODE>{self.result_code()}</MNT_RESULT_CODE>
            <MNT_DESCRIPTION></MNT_DESCRIPTION>
            <MNT_AMOUNT>{self.amount}</MNT_AMOUNT>
            <MNT_SIGNATURE>{self.get_signature(account_code)}</MNT_SIGNATURE>
        </MNT_RESPONSE>
                """
