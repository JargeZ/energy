from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from energy.customers.tests.utils.create_blue_customer import create_blue_customer
from energy.customers.tests.utils.create_green_customer import create_green_customer
from energy.suppliers.tests.utils.create_blue_supplier import create_blue_supplier
from energy.suppliers.tests.utils.create_green_supplier import create_green_supplier
from energy.tests.factory.UserFactory import UserFactory


class Command(BaseCommand):
    help = "Seed demo data"

    def handle(self, *args, **options):
        if User.objects.count() > 0:
            raise CommandError("Demo data already exists")

        create_blue_supplier()
        create_blue_customer()
        create_green_supplier()
        create_green_customer()

        UserFactory(username="demo", password='demo', is_superuser=True, is_staff=True)
