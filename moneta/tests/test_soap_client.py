import datetime
import os

import pytest

from moneta.configuration.soap_client import SoapClient


def get_soap_client():
    login = os.environ.get("MNT_LOGIN")
    pwd = os.environ.get("MNT_PWD")
    url = "https://service.moneta.ru/services.wsdl"
    return SoapClient(url=url, login=login, password=pwd)


def test_get_operation_list():
    now = datetime.datetime.now()
    day_ago = now - datetime.timedelta(days=1)
    client = get_soap_client()
    client.debug_mode()
    response = client.get_operation_list(day_ago, now)
    assert response is not None


def test_get_sum_per_period():
    now = datetime.datetime.now()
    day_ago = now - datetime.timedelta(days=1)
    client = get_soap_client()
    response = client.get_sum_per_period(day_ago, now)
    assert response > 0

