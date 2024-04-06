import pytest
import rest_framework.test
from django.contrib.auth.models import User
from energy.customers.models_factory import CustomerFactory
from energy.customers.tests.utils.create_blue_customer import create_blue_customer
from energy.suppliers.tests.utils.create_blue_supplier import create_blue_supplier
from energy.tests.factory.UserFactory import UserFactory


class BaseEnergyTest:
    @pytest.fixture()
    def whole_data(self, db) -> None:
        self._user_admin = UserFactory()
        self._customer = CustomerFactory()

    @pytest.fixture()
    def user_admin(self, whole_data) -> User:
        return self._user_admin

    @pytest.fixture()
    def blue_supplier(self, db):
        return create_blue_supplier()

    @pytest.fixture()
    def blue_customer(self, db):
        return create_blue_customer()


    @pytest.fixture()
    def admin_client(
            self,
            db: None,
            user_admin,
    ) -> rest_framework.test.APIClient:
        """A Django test client logged in as an admin user."""
        from rest_framework.test import APIClient

        client = APIClient()
        client.force_authenticate(user_admin)
        return client
