from django.db import models
from energy.consumption.models import EnergyQuantile


class Customer(models.Model):
    business_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    energy_quantiles: models.QuerySet[EnergyQuantile]

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return f"{self.business_name} {self.address}"
