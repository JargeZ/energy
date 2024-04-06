import factory
from django.contrib.auth import get_user_model
from factory import post_generation
from factory.django import DjangoModelFactory
from faker import Faker

faker = Faker()


class UserFactory(DjangoModelFactory):
    phone = factory.LazyAttribute(lambda obj: faker.phone_number())
    email = factory.LazyAttribute(lambda obj: faker.email())
    first_name = factory.LazyAttribute(lambda obj: faker.first_name())
    last_name = factory.LazyAttribute(lambda obj: faker.last_name())

    class Meta:
        model = get_user_model()

    @post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("defaultpassword")
        self.save()
