import pytest
from pydantic import ValidationError
from moneta.configuration import (
    BasicConfig,
    UrlsConfig,
    MainConfig,
    MainSettings,
)


def test_empty_basic_config():
    with pytest.raises(ValidationError):
        empty_config = {}
        BasicConfig(**empty_config)


def test_normal_basic_config():
    normal_config = {
        "account_id": 123,
        "account_username": "test",
        "account_password": "test",
    }
    cfg = BasicConfig(**normal_config)
    assert cfg.account_id == 123
    assert cfg.account_username == "test"
    assert cfg.account_password == "test"


def test_urls_config():
    cfg = UrlsConfig()
    assert cfg.production_url == "https://service.moneta.ru"
    with pytest.raises(ValidationError):
        UrlsConfig(demo_url="bad_str")


def test_main_config():
    config = {
        "basic_config": {
            "account_id": 123,
            "account_username": "test",
            "account_password": "test",
        },
        "urls_config": {},
    }
    cfg = MainConfig(**config)
    assert cfg.basic_config.account_id == 123
    assert cfg.basic_config.account_username == "test"
    assert cfg.basic_config.account_password == "test"


def test_payment_url():
    config = {
        "basic_config": {
            "account_id": 123,
            "account_username": "test",
            "account_password": "test",
        },
        "urls_config": {},
    }
    cfg = MainConfig(**config)
    assert cfg.payment_url == "https://demo.moneta.ru"

    config_1 = {
        "basic_config": {
            "demo_mode": False,
            "account_id": 123,
            "account_username": "test",
            "account_password": "test",
        },
        "urls_config": {},
    }
    cfg1 = MainConfig(**config_1)
    assert cfg1.payment_url == "https://service.moneta.ru"

    config_2 = {
        "basic_config": {
            "account_id": 123,
            "account_username": "test",
            "account_password": "test",
        },
        "urls_config": {
            "demo_url": "https://ya.ru",
        },
    }
    cfg2 = MainConfig(**config_2)
    assert cfg2.payment_url == "https://ya.ru"


def test_correct_main_settings():
    user_settings = {
        "basic_config": {
            "account_id": 123,
            "account_username": "test",
            "account_password": "test",
        }
    }
    settings = MainSettings(user_settings=user_settings)
    assert settings.payment_url == "https://demo.moneta.ru"
    assert settings.basic_config.account_id == 123
    with pytest.raises(AttributeError):
        assert settings.empty_attr is None


def test_empty_main_settings():
    with pytest.raises(ValidationError):
        MainSettings(user_settings={})


def test_incorrect_payment_system_name():
    config = {
        "basic_config": {
            "account_id": 123,
            "account_username": "test",
            "account_password": "test",
            "payment_system_name": "super-duper",
        }
    }
    with pytest.raises(ValueError):
        MainSettings(user_settings=config)
