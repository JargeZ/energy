from energy.tariffs.models import TariffCondition, Tariff, TariffGroup
from factory.django import DjangoModelFactory


class TariffConditionFactory(DjangoModelFactory):
    class Meta:
        model = TariffCondition


class TariffFactory(DjangoModelFactory):
    class Meta:
        model = Tariff


class TariffGroupFactory(DjangoModelFactory):
    class Meta:
        model = TariffGroup
