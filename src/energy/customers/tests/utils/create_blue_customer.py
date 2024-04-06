from datetime import datetime
from zoneinfo import ZoneInfo

from energy.consumption.models_factory import EnergyQuantileFactory
from energy.customers.models import Customer
from energy.customers.models_factory import CustomerFactory
from energy.tariffs.models import EnergyType


def create_blue_customer() -> Customer:
    # reverse analysis of the Blue customer bill sheet
    # TODO: automate as bill-parsers and flatten equally for whole period

    customer = CustomerFactory(business_name="Blue customer")

    PEAK_ENERGY_BUT_OFF_PEAK_NETWORK = 6_927.9400 - 6_372.3280  # = 555.6120
    OFF_PEAK_BOOTH = min(3_229.5760, 3_785.1880)  # = 3_229.5760
    PEAK_BOOTH = min(6_927.9400, 6_372.3280)  # = 6_372.3280

    #  - 00:00:00
    #  |
    #  |  [OFF_PEAK_BOOTH]
    #  |
    #  |  - 09:00 - start ENERGY Peak
    #  |
    #  |   [PEAK_ENERGY_BUT_OFF_PEAK_NETWORK]
    #  |
    #  |  - 15:00 - start NETWORK Peak
    #  |
    #  |   [PEAK_BOOTH]
    #  |
    #  |  - 19:00 -  end ENERGY Peak
    #  |
    #  |
    #  | - 22:00 - end NETWORK Peak
    #  |
    #  |
    #  - 23:59:59

    # OFF_PEAK_BOOTH
    EnergyQuantileFactory(
        customer=customer,
        start=datetime(2024, 1, 4, 1, 33, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        end=datetime(2024, 1, 4, 8, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        type=EnergyType.KWH.value,
        value=OFF_PEAK_BOOTH,
    )

    # PEAK_ENERGY_BUT_OFF_PEAK_NETWORK
    EnergyQuantileFactory(
        customer=customer,
        start=datetime(2024, 1, 4, 10, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        end=datetime(2024, 1, 4, 13, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        type=EnergyType.KWH.value,
        value=PEAK_ENERGY_BUT_OFF_PEAK_NETWORK,
    )

    # PEAK_BOOTH
    EnergyQuantileFactory(
        customer=customer,
        start=datetime(2024, 1, 4, 16, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        end=datetime(2024, 1, 4, 17, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        type=EnergyType.KWH.value,
        value=PEAK_BOOTH,
    )

    # Summer DEMAND for month
    EnergyQuantileFactory(
        customer=customer,
        start=datetime(2024, 1, 1, 0, 0, 0, tzinfo=ZoneInfo("Australia/Sydney")),
        end=datetime(2024, 1, 31, 23, 59, 59, tzinfo=ZoneInfo("Australia/Sydney")),
        type=EnergyType.KW.value,
        value=34.1600,
    )

    return customer
