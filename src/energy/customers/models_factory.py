# mypy: disable-error-code="assignment"

import factory
from factory.django import DjangoModelFactory

from energy.customers.models import Customer


class CustomerFactory(DjangoModelFactory):
    business_name: str = factory.Faker("company")
    email: str = factory.Faker("email")
    phone: str = factory.Faker("phone_number")
    address: str = factory.Faker("address")

    class Meta:
        model = Customer
