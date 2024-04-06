from energy.suppliers.models import EnergySupplier
from factory import fuzzy
from factory.django import DjangoModelFactory


class EnergySupplierFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=255)

    class Meta:
        model = EnergySupplier
