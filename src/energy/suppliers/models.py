from django.db import models
from energy.tariffs.models import Tariff


class EnergySupplier(models.Model):
    name = models.CharField(max_length=255)

    tariffs: models.QuerySet[Tariff]

    class Meta:
        db_table = 'energy_supplier'

    def __str__(self):
        return self.name
