from django.db import models
from django.db.models import CheckConstraint, Q

from energy.tariffs.models import EnergyType


class EnergyConsumptionRecord(models.Model):
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, related_name="energy_quantiles")

    start = models.DateTimeField()
    end = models.DateTimeField()

    type = models.CharField(max_length=255, choices=EnergyType.choices)
    value = models.DecimalField(verbose_name="Consumed value", max_digits=15, decimal_places=10)

    class Meta:
        db_table = "energy_quantile"
        constraints = [
            CheckConstraint(
                check=Q(start__lte=models.F("end")),
                name="start_less_than_or_equal_to_end",
            ),
        ]

    def __str__(self):
        diff = self.end - self.start

        return f"{self.customer.business_name} {self.type} {diff}"
