from datetime import datetime
from decimal import Decimal

from energy.customers.models import Customer
from energy.suppliers.models import EnergySupplier


class CalculatorService:
    def __init__(self, supplier: EnergySupplier, customer: Customer):
        self.supplier = supplier
        self.customer = customer

    def calculate_total(self, from_date: datetime, to_date: datetime) -> Decimal:
        pass
