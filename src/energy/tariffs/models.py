from datetime import datetime
from enum import Enum

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q

from energy.utils.enum_to_choises import EnumChoiceMixin

WEEKDAY_RANGE_VALIDATORS = [MinValueValidator(1), MaxValueValidator(7)]


class EnergyType(EnumChoiceMixin, Enum):
    KW = "KW"
    KWH = "kWh"
    KWA = "kWA"


# TODO: deduplicate but may be enough, should be not so often changing
class UnitType(EnumChoiceMixin, Enum):
    KW = "KW"
    KWH = "kWh"
    KWA = "kWA"

    DAYS = "days"
    FIXED = "fixed"


class TariffCondition(models.Model):
    class Type(EnumChoiceMixin, Enum):
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

    weekday_from = models.IntegerField(null=True, blank=True, validators=WEEKDAY_RANGE_VALIDATORS)
    weekday_to = models.IntegerField(null=True, blank=True, validators=WEEKDAY_RANGE_VALIDATORS)

    class Meta:
        db_table = "tariff_condition"
        constraints = [
            CheckConstraint(
                check=(
                    Q(type="time_range") & Q(time_from__isnull=False, time_to__isnull=False)
                    | Q(type="date_range") & Q(date_from__isnull=False, date_to__isnull=False)
                    | Q(type="mixed")
                    & Q(date_from__isnull=False, date_to__isnull=False, time_from__isnull=False, time_to__isnull=False)
                    | Q(type="weekday_range") & Q(weekday_from__isnull=False, weekday_to__isnull=False)
                ),
                name="ranges_fields",
            ),
            CheckConstraint(
                name="weekday_from_1_to_7_or_null",
                check=(
                    Q(weekday_from__gte=1, weekday_from__lte=7, weekday_to__gte=1, weekday_to__lte=7)
                    | Q(weekday_from__isnull=True, weekday_to__isnull=True)
                ),
            ),
        ]

    def is_match(self, from_date: datetime, to_date: datetime) -> bool:
        matches: list[bool] = []
        if self.weekday_from and self.weekday_to:
            matches.append(self.weekday_from <= from_date.isoweekday() <= self.weekday_to)

        if self.date_from and self.date_to:
            from_match = self.date_from <= from_date.date() <= self.date_to
            to_match = self.date_from <= to_date.date() <= self.date_to
            matches.append(from_match or to_match)

        if self.time_from and self.time_to:
            from_match = self.time_from <= from_date.time() <= self.time_to
            to_match = self.time_from <= to_date.time() <= self.time_to
            matches.append(from_match or to_match)

        if self.type != TariffCondition.Type.MIXED:
            assert len(matches) == 1

        return not all(matches) if self.inverted else all(matches)


# Namespace for tariffs in which they should be uniq.
# e.g. if we have tariffs for energy and for network, they should be in different groups
# and so consumption calculator will apply consumption to all tariffs across different groups
# but only one tariff from the same group should be matched
class TariffGroup(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "tariff_group"


class Tariff(models.Model):
    supplier = models.ForeignKey("suppliers.EnergySupplier", on_delete=models.CASCADE, related_name="tariffs")
    name = models.CharField(max_length=255)

    unit_price = models.DecimalField(max_digits=15, decimal_places=10)
    unit_type = models.CharField(max_length=255, choices=UnitType.choices)
    effective_after_consumption = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    priority = models.IntegerField(default=0)
    group = models.ForeignKey(TariffGroup, on_delete=models.CASCADE, null=False, blank=False)
    group_id: int

    consumption_coefficient = models.DecimalField(max_digits=10, decimal_places=5, default=1)

    # NOTE: Possible many (but need to clarify AND/OR logic)
    condition: TariffCondition | None = models.ForeignKey(
        TariffCondition, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "tariff"
        constraints = [
            CheckConstraint(
                name="effective_after_consumption_positive",
                check=Q(effective_after_consumption__gte=0),
            ),
            CheckConstraint(
                name="condition_set_for_kwh",
                check=(
                    Q(unit_type="kWh") & Q(condition__isnull=False)
                    | Q(unit_type="KW") & Q(condition__isnull=False)
                    | Q(unit_type="kWA") & Q(condition__isnull=False)
                    | Q(unit_type="days") & Q(condition__isnull=True)
                    | Q(unit_type="fixed") & Q(condition__isnull=True)
                ),
            ),
        ]
