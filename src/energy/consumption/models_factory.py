import factory
from energy.consumption.models import EnergyQuantile
from energy.tariffs.models import EnergyType
from factory import fuzzy
from factory.django import DjangoModelFactory


class EnergyQuantileFactory(DjangoModelFactory):
    start = factory.Faker('date_time')
    end = factory.Faker("text")

    type = fuzzy.FuzzyChoice(EnergyType.choices)
    value = fuzzy.FuzzyDecimal(0.0, 100.0)

    class Meta:
        model = EnergyQuantile
