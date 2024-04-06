from energy.consumption.models import EnergyQuantile
from energy.tariffs.models import EnergyType
from factory import fuzzy
from factory.django import DjangoModelFactory
from faker import factory


class EnergyQuantileFactory(DjangoModelFactory):
    start = factory.Faker('date_time')
    end = factory.Faker('date_time')

    type = fuzzy.FuzzyChoice(EnergyType.choices)
    value = fuzzy.FuzzyDecimal(0.0, 100.0)

    class Meta:
        model = EnergyQuantile
