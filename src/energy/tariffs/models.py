from datetime import date, datetime, time
from enum import Enum
from typing import Annotated, Optional

from annotated_types import Len
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_pydantic_field import SchemaField
from pydantic import RootModel

from energy.utils.enum_to_choises import EnumChoiceMixin

WEEKDAY_RANGE_VALIDATORS = [MinValueValidator(1), MaxValueValidator(7)]


# TODO: cleanup file


class EnergyType(EnumChoiceMixin, Enum):
    KW = "KW"
    KWH = "kWh"
    KVA = "kVA"


# TODO: deduplicate but may be enough, should be not so often changing
class UnitType(EnumChoiceMixin, Enum):
    KW = "KW"
    KWH = "kWh"
    KVA = "kVA"

    DAYS = "days"
    FIXED = "fixed"


class ConditionValue(RootModel):
    root: Optional[
        Annotated[list[int], Len(min_length=2)]
        | Annotated[list[date], Len(min_length=2)]
        | Annotated[list[time], Len(min_length=2)]
        | datetime
        | int
    ]


class ActivationRule(models.Model):
    class Parameter(EnumChoiceMixin):
        DATE = "date"
        TIME = "time"
        WEEKDAY = "weekday"
        CONSUMED = "consumed"

    class Operator(EnumChoiceMixin, Enum):
        EQ = "eq"
        IN = "in"
        NOT_IN = "not_in"
        BETWEEN = "between"
        NOT_BETWEEN = "not_between"

    name = models.CharField(max_length=255)

    parameter = models.CharField(max_length=255, choices=Parameter.choices)
    operator = models.CharField(max_length=255, choices=Operator.choices)

    # TODO: can be normalized, extract list values in separate shareable model and so on
    value: ConditionValue = SchemaField(null=True, blank=True)  # type: ignore[assignment]

    def __str__(self):
        return f"{self.name} - {self.parameter} {self.operator} {self.value.root}"[:100]


# Namespace for tariffs in which they should be uniq.
# e.g. if we have tariffs for energy and for network, they should be in different groups
# and so consumption calculator will apply consumption to all tariffs across different groups
# but only one tariff from the same group should be matched
class TariffGroup(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "tariff_group"

    def __str__(self):
        return self.name


class Tariff(models.Model):
    supplier = models.ForeignKey("suppliers.EnergySupplier", on_delete=models.CASCADE, related_name="tariffs")
    name = models.CharField(max_length=255)

    unit_price = models.DecimalField(max_digits=15, decimal_places=10)
    unit_type = models.CharField(max_length=255, choices=UnitType.choices)
    priority = models.IntegerField(default=0)
    group = models.ForeignKey(TariffGroup, on_delete=models.CASCADE, null=False, blank=False)
    group_id: int  # never mind, just fast way for IDE

    # not sure about it, just for deal with Loss factor at the moment
    consumption_coefficient = models.DecimalField(max_digits=10, decimal_places=5, default=1)

    activation_rules = models.ManyToManyField(ActivationRule, related_name="tariffs")

    class Meta:
        db_table = "tariff"
        unique_together = [
            ("priority", "group"),
        ]
