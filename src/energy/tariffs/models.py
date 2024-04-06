from django.db import models
from django.db.models import CheckConstraint, Q


class TariffType(models.Choices):
    TIME_RANGE = "time_range"
    DATE_RANGE = "date_range"
    MIXED = "mixed"

class UnitType(models.Choices):
    KWH = "kWh"
    DAY = "day"
    FIXED = "fixed"

class TariffCondition(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    # TODO: possible normalize by creating a separate model for each type
    time_from = models.TimeField(null=True, blank=True)
    time_to = models.TimeField(null=True, blank=True)

    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(type='time_range', time_from__isnull=False, time_to__isnull=False),
                name='time_range_fields_not_null',
            ),
            CheckConstraint(
                check=Q(type='date_range', date_from__isnull=False, date_to__isnull=False),
                name='date_range_fields_not_null',
            ),
            CheckConstraint(
                check=Q(type='mixed', date_from__isnull=False, date_to__isnull=False, time_from__isnull=False, time_to__isnull=False),
                name='mixed_range_fields_not_null',
            ),

        ]


class Tariff(models.Model):
    supplier = models.ForeignKey('suppliers.EnergySupplier', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_type = models.CharField(max_length=255)
    effective_after_consumption = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    priority = models.IntegerField()
    stackable = models.BooleanField()

    # NOTE: Possible many (but need to clarify AND/OR logic)
    condition = models.ForeignKey(TariffCondition, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(effective_after_consumption__gte=0),
                name='effective_after_consumption_positive',
            ),
        ]