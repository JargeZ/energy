from datetime import date
from decimal import Decimal

from energy.suppliers.models import EnergySupplier
from energy.suppliers.models_factory import EnergySupplierFactory
from energy.tariffs.models import ActivationRule, UnitType
from energy.tariffs.models_factory import (
    ActivationRuleFactory,
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
        priority=1,
        supplier=supplier,
        group=energy_charges,
        name="Off-peak base energy charge",
        unit_type=UnitType.KWH.value,
        unit_price=0.063960,
        consumption_coefficient=LOSS_FACTOR,
        activation_rules=[
            # Base rule last by priority
        ],
    )
    TariffFactory(
        priority=2,
        supplier=supplier,
        group=energy_charges,
        name="Peak energy charge",
        unit_type=UnitType.KWH.value,
        unit_price=0.077990,
        consumption_coefficient=LOSS_FACTOR,
        activation_rules=[
            ActivationRuleFactory(
                name="Peak energy time",
                parameter=ActivationRule.Parameter.TIME.value,
                operator=ActivationRule.Operator.BETWEEN.value,
                value=["09:00:00", "19:00:00"],
            )
        ],
    )

    network_charges = TariffGroupFactory(name="Network charges")
    # NETWORK CHARGES
    TariffFactory(
        priority=0,
        supplier=supplier,
        group=network_charges,
        name="Daily network charge",
        unit_type=UnitType.DAYS.value,
        unit_price=3.288000,
    )
    TariffFactory(
        priority=1,
        supplier=supplier,
        group=network_charges,
        name="Off-peak base network charge",
        unit_type=UnitType.KWH.value,
        unit_price=0.045300,
        activation_rules=[],
    )
    TariffFactory(
        priority=2,
        supplier=supplier,
        group=network_charges,
        name="Peak network charge",
        unit_type=UnitType.KWH.value,
        unit_price=0.045300,
        activation_rules=[
            ActivationRuleFactory(
                name="Peak energy time",
                parameter=ActivationRule.Parameter.TIME.value,
                operator=ActivationRule.Operator.BETWEEN.value,
                value=["15:00:00", "22:00:00"],
            )
        ],
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
        activation_rules=[
            ActivationRuleFactory(
                name="Summer demand time",
                parameter=ActivationRule.Parameter.DATE.value,
                operator=ActivationRule.Operator.BETWEEN.value,
                value=[date(2023, 11, 30), date(2024, 3, 1)],
            )
        ],
    )

    return supplier
