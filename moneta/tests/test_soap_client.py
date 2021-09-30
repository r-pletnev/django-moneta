import datetime
import os
from collections import OrderedDict

import pydash
import pytest

from moneta.configuration.soap_client import SoapClient


def get_soap_client():
    login = os.environ.get("MNT_LOGIN")
    pwd = os.environ.get("MNT_PWD")
    url = "https://service.moneta.ru/services.wsdl"
    return SoapClient(url=url, login=login, password=pwd)


def test_get_operation_list():
    d1 = datetime.datetime(2021,9,22)
    d2 = datetime.datetime(2021,9, 22,23,59,59)
    client = get_soap_client()
    client.debug_mode()
    result = client.get_operations(d1, d2)
    assert result is not None
    assert isinstance(pydash.get(result, '0'), dict)
    assert isinstance(pydash.get(result, '0'), OrderedDict) is False
    assert isinstance(pydash.get(result, '0.id'), int)
    assert isinstance(pydash.get(result, '0.sourceamount'), int)


def test_get_sum_per_period():
    d1 = datetime.datetime(2021,9,22)
    d2 = datetime.datetime(2021,9, 22,23,59,59)
    client = get_soap_client()
    response = client.get_sum_per_period(d1, d2)
    assert response > 0

