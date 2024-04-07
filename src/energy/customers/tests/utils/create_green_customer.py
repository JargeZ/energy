from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from energy.consumption.models_factory import EnergyQuantileFactory
from energy.customers.models import Customer
from energy.customers.models_factory import CustomerFactory
from energy.tariffs.models import EnergyType
from energy.utils.power_converters import kVA_to_kW


def create_green_customer() -> Customer:
    # reverse analysis of the Green customer bill sheet
    customer = CustomerFactory(business_name="Green customer")

    # Whole month base energy
    EnergyQuantileFactory(
        customer=customer,
        start=datetime(2024, 2, 28, 0, 0, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        end=datetime(2024, 3, 26, 0, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        type=EnergyType.KWH.value,
        value=Decimal("739.80") + Decimal("5392.50"),
    )

    # Demand workday
    EnergyQuantileFactory(
        customer=customer,
        start=datetime(2024, 3, 21, 10, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        end=datetime(2024, 3, 21, 13, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        type=EnergyType.KVA.value,
        value=Decimal("594.39"),
    )
    # Demand non workday (weekend)
    EnergyQuantileFactory(
        customer=customer,
        start=datetime(2024, 3, 23, 10, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        end=datetime(2024, 3, 23, 13, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        type=EnergyType.KVA.value,
        value=Decimal("202.86"),
    )

    return customer
