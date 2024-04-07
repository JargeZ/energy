# mypy: disable-error-code="assignment"

import factory
from django.contrib.auth import get_user_model
from factory import post_generation
from factory.django import DjangoModelFactory
from faker import Faker

faker = Faker()


class UserFactory(DjangoModelFactory):
    email: str = factory.LazyAttribute(lambda obj: faker.email())
    first_name: str = factory.LazyAttribute(lambda obj: faker.first_name())
    last_name: str = factory.LazyAttribute(lambda obj: faker.last_name())
    is_active: bool = True

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
