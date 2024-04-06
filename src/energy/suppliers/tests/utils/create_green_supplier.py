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
from energy.utils.power_converters import kVA_to_kW


def create_green_supplier() -> EnergySupplier:
    supplier = EnergySupplierFactory(name="Green")

    # ENERGY CHARGES
    energy_charges = TariffGroupFactory(name="Energy charges")
    TariffFactory(
        supplier=supplier,
        group=energy_charges,
        name="Base energy charge - step 1",
        unit_type=UnitType.KWH.value,
        unit_price=0.063960,
        condition=TariffConditionFactory(
            name="Off-peak energy time",
            type=TariffCondition.Type.TIME_RANGE.value,
            time_from="09:00:00",
            time_to="19:00:00",
            inverted=True,
        ),
    )
    # TariffFactory(
    #     supplier=supplier,
    #     group=energy_charges,
    #     name="Peak energy charge",
    #     unit_type=UnitType.KWH.value,
    #     unit_price=0.077990,
    #     consumption_coefficient=LOSS_FACTOR,
    #     condition=TariffConditionFactory(
    #         name="Peak energy time",
    #         type=TariffCondition.Type.TIME_RANGE.value,
    #         time_from="09:00:00",
    #         time_to="19:00:00",
    #     ),
    # )

    network_charges = TariffGroupFactory(name="Network charges")
    # NETWORK CHARGES
    TariffFactory(
        supplier=supplier,
        group=network_charges,
        name="Network Demand usage",
        unit_type=UnitType.KW.value,
        unit_price=kVA_to_kW(Decimal("0.0795")),
        condition=TariffConditionFactory(
            name="Demand base days time",
            type=TariffCondition.Type.MIXED.value,
            time_from=time(9, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
            time_to=time(21, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
            weekday_from=1,
            weekday_to=5,
            inverted=True,  # <- this is the only difference TODO abstract
        ),
    )
    TariffFactory(
        supplier=supplier,
        group=network_charges,
        name="Network Demand usage",
        unit_type=UnitType.KW.value,
        unit_price=kVA_to_kW(Decimal("0.0795")),
        condition=TariffConditionFactory(
            name="Demand base days time",
            type=TariffCondition.Type.MIXED.value,
            time_from=time(9, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
            time_to=time(21, 00, 00, tzinfo=ZoneInfo("Australia/Sydney")),
            weekday_from=1,
            weekday_to=5,
            inverted=False,  # <- this is the only difference TODO abstract
        ),
    )

    # METERS AND DEMAND
    meters = TariffGroupFactory(name="Meters")
    TariffFactory(
        supplier=supplier,
        group=meters,
        name="Daily metering charge",
        # TODO: seems like not fixed. Need to clarify dependency
        unit_type=UnitType.FIXED.value,
        unit_price=91.65,
    )
    # METERS AND DEMAND
    service_to_property = TariffGroupFactory(name="Service to property")
    TariffFactory(
        supplier=supplier,
        group=service_to_property,
        name="Service to property charge",
        unit_type=UnitType.DAYS.value,
        unit_price=Decimal("5.7839"),
    )

    return supplier
