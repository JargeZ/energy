from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q

WEEKDAY_RANGE_VALIDATORS = [
    MinValueValidator(1),
    MaxValueValidator(7)
]


class UnitType(models.Choices):
    KW = "KW"
    KWH = "kWh"
    KWA = "kWA"
    DAYS = "days"
    FIXED = "fixed"


class TariffCondition(models.Model):
    class Type(models.Choices):
        TIME_RANGE = "time_range"
        DATE_RANGE = "date_range"
        WEEKDAY_RANGE = "weekday_range"
        MIXED = "mixed"

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=Type.choices)

    # TODO: possible more complex structure
    inverted = models.BooleanField("Not in range", default=False)

    # TODO: possible normalize by creating a separate model for each type
    time_from = models.TimeField(null=True, blank=True)
    time_to = models.TimeField(null=True, blank=True)

    # NOTE: year may be redundant byt most likely no because of changing of tariffs every year or month
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)

    weekday_from = models.IntegerField(
        null=True,
        blank=True,
        validators=WEEKDAY_RANGE_VALIDATORS
    )
    weekday_to = models.IntegerField(
        null=True,
        blank=True,
        validators=WEEKDAY_RANGE_VALIDATORS
    )

    class Meta:
        db_table = 'tariff_condition'
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
                check=Q(type='mixed', date_from__isnull=False, date_to__isnull=False, time_from__isnull=False,
                        time_to__isnull=False),
                name='mixed_range_fields_not_null',
            ),
            CheckConstraint(
                check=Q(type='weekday_range', weekday_from__isnull=False, weekday_to__isnull=False),
                name='weekday_range_fields_not_null',
            ),
            CheckConstraint(
                name='weekday_from_1_to_7',
                check=Q(weekday_from__gte=1, weekday_from__lte=7, weekday_to__gte=1, weekday_to__lte=7),
            ),
        ]


class Tariff(models.Model):
    supplier = models.ForeignKey('suppliers.EnergySupplier', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    unit_price = models.DecimalField(max_digits=10, decimal_places=10)
    unit_type = models.CharField(max_length=255, choices=UnitType.choices)
    effective_after_consumption = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    priority = models.IntegerField(default=0)
    # stackable = models.BooleanField(default=False)

    # NOTE: Possible many (but need to clarify AND/OR logic)
    condition = models.ForeignKey(TariffCondition, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'tariff'
        constraints = [
            CheckConstraint(
                name='effective_after_consumption_positive',
                check=Q(effective_after_consumption__gte=0),
            ),
            CheckConstraint(
                name='condition_set_for_kwh',
                check=Q(unit_type='kWh', condition__isnull=False),
            ),
        ]
