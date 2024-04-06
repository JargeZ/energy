from django.db import models


class EnergySupplier(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'energy_supplier'

    def __str__(self):
        return self.name
