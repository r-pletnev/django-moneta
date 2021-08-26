import datetime

from suds.client import Client
import suds.wsse as wsse

import logging


class SoapClient:
    def __init__(self, url: str, login: str, password: str):
        self.client = Client(url, cache=None)
        security = wsse.Security()
        token = wsse.UsernameToken(login, password)
        security.tokens.append(token)
        self.client.set_options(wsse=security, port="MessagesSoap11")

    @staticmethod
    def debug_mode():
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("suds.client").setLevel(logging.DEBUG)

    def get_operation_list(
        self, from_date: datetime.datetime, date_to: datetime.datetime
    ) -> list:
        ftr = {"dateFrom": from_date, "dateTo": date_to}
        response = self.client.service.FindOperationsList(filter=ftr)
        return response
