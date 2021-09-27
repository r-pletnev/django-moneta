import urllib.parse
from django.conf import settings as django_settings
from django.utils.functional import SimpleLazyObject
from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, Union

from moneta.models import PaymentSystem


class BasicConfig(BaseModel):
    demo_mode: Optional[bool] = True
    test_mode: Optional[bool] = True
    debug_mode: Optional[bool] = True
    account_id: int
    account_code: Optional[str] = None
    account_username: str
    account_password: str
    prototype_user_unit_id: Optional[str] = None
    history_items_per_page: Optional[int] = 20
    currency: Optional[str] = "RUB"
    payment_description: Optional[str] = None
    payment_system_name: Optional[str] = "plastic"
    signature_required: Optional[bool] = False

    def get_account_code(self) -> str:
        if self.account_code is None:
            return ""
        return str(self.account_code)

    def get_test_mode(self) -> str:
        return str(int(self.test_mode))

    @validator("payment_system_name")
    def checkin_payment_system_id(cls, v):
        if not PaymentSystem.objects.filter(name=v).exists():
            raise ValueError("payment system not found")
        return v


class UrlsConfig(BaseModel):
    demo_url: Optional[HttpUrl] = "https://demo.moneta.ru"
    production_url: Optional[HttpUrl] = "https://service.moneta.ru"
    success_url: Optional[str] = None
    fail_url: Optional[str] = None
    inprogress_url: Optional[str] = None
    return_url: Optional[str] = None
    iframe_target: Optional[str] = "_parent"
    assistant_link: Optional[str] = "/assistant.htm"
    soap_link: Optional[str] = "/services.wsdl"
    json_link: Optional[str] = "/services"
    assistant_widget_link: Optional[str] = "assistant.widget"
    x509_port: Optional[int] = 8443
    x509_soap_link: Optional[str] = "/services/x509.wsdl"
    x509_json_link: Optional[str] = "/services/x509"


class MainConfig(BaseModel):
    basic_config: BasicConfig
    urls_config: UrlsConfig

    @property
    def payment_url(self) -> str:
        if self.basic_config.demo_mode:
            return self.urls_config.demo_url
        return self.urls_config.production_url

    @property
    def soap_url(self) -> str:
        return urllib.parse.urljoin(self.payment_url, self.urls_config.soap_link)


    def get_payment_description(self) -> Optional[str]:
        return self.basic_config.payment_description

    @property
    def payment_system(self) -> PaymentSystem:
        pay_system = PaymentSystem.objects.filter(
            name=self.basic_config.payment_system_name
        ).last()
        return pay_system

    def __getattr__(self, item):
        return getattr(self.basic_config, item)


DEFAULTS = {
    "basic_config": {},
    "urls_config": {},
}


class MainSettings:
    def __init__(self, user_settings: dict, defaults=None):
        if defaults is None:
            defaults = DEFAULTS
        config = {**defaults, **user_settings}
        self._config = MainConfig(**config)

    def __getattr__(self, attr: str) -> Union[str, int]:
        return getattr(self._config, attr)

    def config(self) -> MainConfig:
        return self._config

    def url_generator(self) -> "UrlGenerator":
        from .url_generator import UrlGenerator

        return UrlGenerator(config=self.config())


class LazyWrapperMonetaConfig:
    def __init__(self):
        self.settings = None

    def __call__(self):
        if self.settings is None:
            self.settings = MainSettings(
                user_settings=getattr(django_settings, "MONETA", {})
            )

    def __getattr__(self, attr: str):
        if self.settings is None:
            self.settings = MainSettings(
                user_settings=getattr(django_settings, "MONETA", {})
            )
            return getattr(self.settings, attr)


def _init_config():
    return MainSettings(user_settings=getattr(django_settings, "MONETA", {}))


moneta_config = SimpleLazyObject(_init_config)
