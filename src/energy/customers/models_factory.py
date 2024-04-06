import factory
from energy.customers.models import Customer
from factory import faker
from factory.django import DjangoModelFactory


class CustomerFactory(DjangoModelFactory):
    business_name = factory.LazyAttribute(lambda obj: faker.company())
    email = factory.LazyAttribute(lambda obj: faker.email())
    phone = factory.LazyAttribute(lambda obj: faker.phone_number())
    address = factory.LazyAttribute(lambda obj: faker.address())

    class Meta:
        model = Customer