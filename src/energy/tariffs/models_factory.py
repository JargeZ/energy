from factory.django import DjangoModelFactory

from energy.tariffs.models import Tariff, TariffCondition, TariffGroup


class TariffConditionFactory(DjangoModelFactory):
    class Meta:
        model = TariffCondition


class TariffFactory(DjangoModelFactory):
    class Meta:
        model = Tariff


class TariffGroupFactory(DjangoModelFactory):
    class Meta:
        model = TariffGroup
