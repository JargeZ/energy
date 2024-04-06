from datetime import date, time
from decimal import Decimal
from zoneinfo import ZoneInfo

from energy.suppliers.models import EnergySupplier
from energy.suppliers.models_factory import EnergySupplierFactory
from energy.tariffs.models import TariffCondition, UnitType
from energy.tariffs.models_factory import (
    TariffConditionFactory,
    TariffFactory,
    TariffGroupFactory,
)


def create_blue_supplier() -> EnergySupplier:
    supplier = EnergySupplierFactory(name="Blue")

    LOSS_FACTOR = Decimal("1.0450")

    # ENERGY CHARGES
    energy_charges = TariffGroupFactory(name="Energy charges")
    TariffFactory(
        supplier=supplier,
        group=energy_charges,
        name="Daily energy charge",
        unit_type=UnitType.DAYS.value,
        unit_price=1.506849,
    )
    TariffFactory(
        supplier=supplier,
        group=energy_charges,
        name="Off-peak base energy charge",
        unit_type=UnitType.KWH.value,
        unit_price=0.063960,
        consumption_coefficient=LOSS_FACTOR,
        condition=TariffConditionFactory(
            name="Off-peak energy time",
            type=TariffCondition.Type.TIME_RANGE.value,
            time_from="09:00:00",
            time_to="19:00:00",
            inverted=True,
        ),
    )
    TariffFactory(
        supplier=supplier,
        group=energy_charges,
        name="Peak energy charge",
        unit_type=UnitType.KWH.value,
        unit_price=0.077990,
        consumption_coefficient=LOSS_FACTOR,
        condition=TariffConditionFactory(
            name="Peak energy time",
            type=TariffCondition.Type.TIME_RANGE.value,
            time_from="09:00:00",
            time_to="19:00:00",
        ),
    )

    network_charges = TariffGroupFactory(name="Network charges")
    # NETWORK CHARGES
    TariffFactory(
        supplier=supplier,
        group=network_charges,
        name="Daily network charge",
        unit_type=UnitType.DAYS.value,
        unit_price=3.288000,
    )
    TariffFactory(
        supplier=supplier,
        group=network_charges,
        name="Off-peak base network charge",
        unit_type=UnitType.KWH.value,
        unit_price=0.045300,
        condition=TariffConditionFactory(
            name="Off-peak network time",
            type=TariffCondition.Type.TIME_RANGE.value,
            time_from=time(15, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
            time_to=time(22, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
            inverted=True,
        ),
    )
    TariffFactory(
        supplier=supplier,
        group=network_charges,
        name="Peak network charge",
        unit_type=UnitType.KWH.value,
        unit_price=0.045300,
        condition=TariffConditionFactory(
            name="Peak network time",
            type=TariffCondition.Type.TIME_RANGE.value,
            time_from=time(15, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
            time_to=time(22, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
        ),
    )

    # METERS AND DEMAND
    meters = TariffGroupFactory(name="Meters")
    TariffFactory(
        supplier=supplier,
        group=meters,
        name="Daily metering charge",
        unit_type=UnitType.DAYS.value,
        unit_price=4.794521,
    )

    demand = TariffGroupFactory(name="Demand charges")
    TariffFactory(
        supplier=supplier,
        group=demand,
        name="Summer demand charge",
        unit_type=UnitType.KW.value,
        unit_price=15.700000,
        condition=TariffConditionFactory(
            name="Summer demand time",
            type=TariffCondition.Type.DATE_RANGE.value,
            date_from=date(2023, 11, 30),
            date_to=date(2024, 3, 1),
        ),
    )

    return supplier
