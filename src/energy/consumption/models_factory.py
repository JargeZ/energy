# mypy: disable-error-code="assignment"

from datetime import datetime
from decimal import Decimal

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from energy.consumption.models import EnergyConsumptionRecord
from energy.tariffs.models import EnergyType


class EnergyQuantileFactory(DjangoModelFactory):
    start: datetime = factory.Faker("date_time")
    end: datetime = factory.Faker("date_time")

    type: str = fuzzy.FuzzyChoice(EnergyType.choices)
    value: Decimal = fuzzy.FuzzyDecimal(0.0, 100.0)

    class Meta:
        model = EnergyConsumptionRecord
