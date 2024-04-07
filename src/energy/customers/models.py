from datetime import datetime
from zoneinfo import ZoneInfo

from django.db import models

from energy.consumption.models import EnergyConsumptionRecord
from timezone_field import TimeZoneField

DEMO_FROM_DATE = datetime(2024, 1, 1, tzinfo=ZoneInfo("Australia/Sydney"))
DEMO_TO_DATE = datetime(2024, 2, 1, tzinfo=ZoneInfo("Australia/Sydney"))


class Customer(models.Model):
    business_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    demo_bill_from = models.DateTimeField(null=True, blank=True, default=DEMO_FROM_DATE)
    demo_bill_to = models.DateTimeField(null=True, blank=True, default=DEMO_TO_DATE)
    time_zone = TimeZoneField(verbose_name="Timezone", default="Australia/Sydney")

    energy_quantiles: models.QuerySet[EnergyConsumptionRecord]

    class Meta:
        db_table = "customer"

    def __str__(self):
        return f"{self.business_name} {self.address}"
