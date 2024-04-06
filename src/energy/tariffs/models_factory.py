from energy.tariffs.models import TariffCondition, Tariff
from factory.django import DjangoModelFactory


class TariffConditionFactory(DjangoModelFactory[TariffCondition]):
    class Meta:
        model = TariffCondition


class TariffFactory(DjangoModelFactory[Tariff]):
    class Meta:
        model = Tariff
