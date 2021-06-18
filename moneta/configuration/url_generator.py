from hashlib import md5
from pydantic import BaseModel
from typing import Optional, Union

from moneta.models import PaymentSystem
from .config import MainConfig
from moneta.utils import add_url_query_params


class QueryPayload(BaseModel):
    account_id: str  # MNT_ID
    transaction_id: str  # MNT_TRANSACTION_ID
    amount: str  # MNT_AMOUNT
    currency: str  # MNT_CURRENCY_CODE
    test_mode: str  # MNT_TEST_MODE
    unit_id: str  # paymentSystem.unitId
    limit_ids: str  # paymentSystem.limitIds
    subscriber_id: Optional[str] = None  # MNT_SUBSCRIBER_ID
    success_url: Optional[str] = None
    description: Optional[str] = None
    signature: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        fields = {
            "account_id": "MNT_ID",
            "transaction_id": "MNT_TRANSACTION_ID",
            "amount": "MNT_AMOUNT",
            "currency": "MNT_CURRENCY_CODE",
            "test_mode": "MNT_TEST_MODE",
            "unit_id": "paymentSystem.unitId",
            "limit_ids": "paymentSystem.limitIds",
            "success_url": "MNT_SUCCESS_URL",
            "description": "MNT_DESCRIPTION",
            "signature": "MNT_SIGNATURE",
            "subscriber_id": "MNT_SUBSCRIBER_ID",
        }


class UrlGenerator(BaseModel):
    config: MainConfig

    @property
    def root_url(self) -> str:
        return f"{self.config.payment_url}{self.config.urls_config.assistant_link}"

    def _signature_chunks(
        self, order_id: str, amount: float, subscriber_id: str
    ) -> str:
        signature_chunks = [
            str(self.config.basic_config.account_id),
            order_id,
            self.format_amount(amount),
            self.config.basic_config.currency,
            subscriber_id,
            self.config.basic_config.get_test_mode(),
            self.config.basic_config.get_account_code(),
        ]
        return "".join(signature_chunks)

    def signature(
        self, order_id: Union[str, int], amount: float, subscriber_id: str
    ) -> Optional[str]:
        if self.config.basic_config.account_code is None:
            return None
        sign = self._signature_chunks(str(order_id), amount, subscriber_id)
        return md5(sign.encode("utf-8")).hexdigest()

    @staticmethod
    def format_amount(amount: float) -> str:
        return f"{round(amount, 2):.2f}"

    def payment_url(
        self,
        order_id: str,
        amount: float,
        subscriber_id: Optional[str] = "",
        payment_system: Optional[PaymentSystem] = None,
        description: Optional[str] = None,
    ) -> str:
        pay_sys = payment_system if payment_system else self.config.payment_system
        order_id = str(order_id)
        query = QueryPayload(
            account_id=str(self.config.basic_config.account_id),
            transaction_id=order_id,
            amount=self.format_amount(amount),
            currency=self.config.basic_config.currency,
            test_mode=self.config.basic_config.get_test_mode(),
            unit_id=pay_sys.unit_id,
            limit_ids=pay_sys.unit_id,
            success_url=self.config.urls_config.success_url,
            description=description
            if description
            else self.config.get_payment_description(),
            signature=self.signature(order_id, amount, subscriber_id),
            subscriber_id=subscriber_id,
        )
        payload = query.dict(by_alias=True, exclude_none=True)
        return add_url_query_params(url=self.root_url, additional_params=payload)

    class Config:
        arbitrary_types_allowed = True
