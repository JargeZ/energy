import factory
from energy.customers.models import Customer
from factory import faker
from factory.django import DjangoModelFactory


class CustomerFactory(DjangoModelFactory):
    business_name = factory.LazyAttribute(lambda obj: factory.Faker('company'))
    email = factory.LazyAttribute(lambda obj: factory.Faker('email'))
    phone = factory.LazyAttribute(lambda obj: factory.Faker('phone_number'))
    address = factory.LazyAttribute(lambda obj: factory.Faker('address'))

    class Meta:
        model = Customer
