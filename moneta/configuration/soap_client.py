import datetime
from typing import List
from collections import OrderedDict
from pydash import py_

import zeep
from zeep.wsse.username import UsernameToken

import logging


class SoapClient:
    def __init__(self, url: str, login: str, password: str):
        token = UsernameToken(login, password)
        self.client = zeep.Client(url, wsse=token)

    @staticmethod
    def debug_mode():
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("suds.client").setLevel(logging.DEBUG)

    def get_operation_list(
        self, date_from: datetime.datetime, date_to: datetime.datetime
    ) -> List[OrderedDict]:
        ftr = {"dateFrom": date_from, "dateTo": date_to}
        response = self.client.service.FindOperationsList(filter=ftr)
        result = zeep.helpers.serialize_object(response)
        return result.get("operation", [])

    def get_sum_per_period(
        self, date_from: datetime.datetime, date_to: datetime.datetime
    ) -> int:
        operations = self.get_operation_list(date_from, date_to)
        return (
            py_(operations)
            .map("attribute")
            .flatten()
            .reject(lambda elm: py_.get(elm, ["key"]) != "sourceamount")
            .map_("value")
            .map(lambda elm: int(elm))
            .sum()
            .value()
        )
