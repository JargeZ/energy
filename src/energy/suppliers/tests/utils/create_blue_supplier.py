from energy.suppliers.models import EnergySupplier
from energy.suppliers.models_factory import EnergySupplierFactory
from energy.tariffs.models import UnitType, TariffCondition
from energy.tariffs.models_factory import TariffFactory, TariffConditionFactory


def create_blue_supplier() -> EnergySupplier:
    supplier = EnergySupplierFactory(name="Blue")

    # ENERGY CHARGES
    TariffFactory(
        supplier=supplier,
        name="Daily energy charge",
        unit_type=UnitType.DAYS,
        unit_price=1.506849,
    )
    TariffFactory(
        supplier=supplier,
        name="Off-peak base energy charge",
        unit_type=UnitType.KWH,
        unit_price=0.063960,
        condition=None,
    )
    TariffFactory(
        supplier=supplier,
        name="Peak energy charge",
        unit_type=UnitType.KWH,
        unit_price=0.077990,
        condition=TariffConditionFactory(
            name="Peak energy time",
            type=TariffCondition.Type.TIME_RANGE,
            time_from="09:00:00",
            time_to="19:00:00",
        ),
    )


    # NETWORK CHARGES
    TariffFactory(
        supplier=supplier,
        name="Daily network charge",
        unit_type=UnitType.DAYS,
        unit_price=3.288000,
    )
    TariffFactory(
        supplier=supplier,
        name="Off-peak base network charge",
        unit_type=UnitType.KWH,
        unit_price=0.045300,
        condition=None
    )
    TariffFactory(
        supplier=supplier,
        name="Peak network charge",
        unit_type=UnitType.KWH,
        unit_price=0.045300,
        condition=TariffConditionFactory(
            name="Off-peak network time",
            type=TariffCondition.Type.TIME_RANGE,
            time_from="15:00:00",
            time_to="22:00:00",
        ),
    )

    # METERS AND DEMAND
    TariffFactory(
        supplier=supplier,
        name="Daily metering charge",
        unit_type=UnitType.DAYS,
        unit_price=4.794521,
    )
    TariffFactory(
        supplier=supplier,
        name="Summer demand charge",
        unit_type=UnitType.KW,
        unit_price=15.700000,
        condition=TariffConditionFactory(
            name="Summer demand time",
            type=TariffCondition.Type.DATE_RANGE,
            date_from="2023-30-11",
            time_to="2024-01-03",
        )
    )

    return supplier
