from django.db import models
from factory.django import DjangoModelFactory


class TariffConditionFactory(DjangoModelFactory):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    # TODO: possible normalize by creating a separate model for each type
    time_from = models.TimeField(null=True, blank=True)
    time_to = models.TimeField(null=True, blank=True)

    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)


class TariffFactory(DjangoModelFactory):
    supplier = models.ForeignKey('suppliers.EnergySupplier', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_type = models.CharField(max_length=255)
    effective_after_consumption = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    priority = models.IntegerField()
    stackable = models.BooleanField()

    # NOTE: Possible many (but need to clarify AND/OR logic)
    condition = models.ForeignKey(TariffCondition, on_delete=models.CASCADE)
