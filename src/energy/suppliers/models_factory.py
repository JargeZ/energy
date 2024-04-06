from factory import fuzzy
from factory.django import DjangoModelFactory

from energy.suppliers.models import EnergySupplier


class EnergySupplierFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=255)

    class Meta:
        model = EnergySupplier
