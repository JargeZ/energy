import factory
from factory.django import DjangoModelFactory

from energy.tariffs.models import ActivationRule, Tariff, TariffGroup


class ActivationRuleFactory(DjangoModelFactory):
    class Meta:
        model = ActivationRule


class TariffFactory(DjangoModelFactory):
    class Meta:
        model = Tariff

    @factory.post_generation
    def activation_rules(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.activation_rules.add(*extracted)


class TariffGroupFactory(DjangoModelFactory):
    class Meta:
        model = TariffGroup
