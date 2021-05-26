from configparser import ConfigParser
from django.core.management.base import BaseCommand

from ...models import PaymentSystem


class Command(BaseCommand):
    help = "Upload file payment_systems.ini to db"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--file",
            required=True,
            help="path to payment_systems.ini"
        )

    def handle(self, *args, **options):
        file_path = options.get("file")
        config = ConfigParser()
        config.read(file_path)
        i = 0
        for section in config.sections():
            values = {}
            values["group"] = config[section]["group"]
            values["title"] = config[section]["title"]
            values["account_id"] = config[section]["accountId"]
            values["unit_id"] = config[section]["unitId"]
            values["create_invoice"] = config[section].getboolean("createInvoice")
            values["name"] = section.replace("monetasdk_paysys_", "")
            
            PaymentSystem.objects.create(**values)
            i += 1
            
        self.stdout.write(self.style.SUCCESS(f"uploaded {i} payment systems"))


