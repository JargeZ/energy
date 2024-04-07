from decimal import Decimal

from energy.suppliers.models import EnergySupplier
from energy.suppliers.models_factory import EnergySupplierFactory
from energy.tariffs.models import ActivationRule, UnitType
from energy.tariffs.models_factory import (
    ActivationRuleFactory,
    TariffFactory,
    TariffGroupFactory,
)
from energy.utils.power_converters import kVA_to_kW

# https://data.gov.au/data/dataset/australian-holidays-machine-readable-dataset
HOLIDAYS = {
    "2024-01-01": "New Year's Day",
    "2024-01-26": "Australia Day",
    "2024-03-04": "Labour Day",
    "2024-05-06": "Labour Day",
    "2024-03-29": "Good Friday",
    "2024-03-30": "Easter Saturday - the day after Good Friday",
    "2024-03-31": "Easter Sunday",
    "2024-04-01": "Easter Monday",
    "2024-04-02": "Easter Tuesday",
    "2024-04-25": "Anzac Day",
    "2024-05-27": "Reconciliation Day",
    "2024-06-03": "Western Australia Day",
    "2024-06-10": "Sovereign's Birthday",
    "2024-08-05": "Bank Holiday",
    "2024-08-14": "Royal Queensland Show (Brisbane only)",
    "2024-09-23": "King's Birthday",
    "2024-09-27": "Friday before the AFL Grand Final",
    "2024-10-07": "King’s Birthday",
    "2024-11-05": "Melbourne Cup",
    "2024-12-24": "Christmas Eve",
    "2024-12-25": "Christmas Day ",
    "2024-12-26": "Boxing Day / Proclamation Day",
    "2024-12-31": "New Year's Eve",
}


def create_green_supplier() -> EnergySupplier:
    supplier = EnergySupplierFactory(name="Green")

    # ENERGY CHARGES
    energy_charges = TariffGroupFactory(name="Energy charges")
    TariffFactory(
        supplier=supplier,
        group=energy_charges,
        priority=1,
        name="Base energy charge - step 1",
        unit_type=UnitType.KWH.value,
        unit_price=0.2178,
        activation_rules=[
            ActivationRuleFactory(
                name="Energy - step 1",
                parameter=ActivationRule.Parameter.CONSUMED.value,
                operator=ActivationRule.Operator.BETWEEN.value,
                value=[0, 739],
            )
        ],
    )
    TariffFactory(
        supplier=supplier,
        group=energy_charges,
        priority=2,
        name="Base energy charge - step 2",
        unit_type=UnitType.KWH.value,
        unit_price=0.2178,
        activation_rules=[
            ActivationRuleFactory(
                name="Energy - step 2",
                parameter=ActivationRule.Parameter.CONSUMED.value,
                operator=ActivationRule.Operator.BETWEEN.value,
                value=[739, 999999],  # TODO: support +Inf
            )
        ],
    )

    network_charges = TariffGroupFactory(name="Network charges")
    # NETWORK CHARGES
    TariffFactory(
        supplier=supplier,
        group=network_charges,
        priority=1,
        name="Base Network Demand usage",
        unit_type=UnitType.KVA.value,
        unit_price=Decimal("0.0795"),
        activation_rules=[],
    )
    TariffFactory(
        supplier=supplier,
        group=network_charges,
        priority=2,
        name="Network Demand usage",
        unit_type=UnitType.KVA.value,
        unit_price=Decimal("0.5128"),
        activation_rules=[
            ActivationRuleFactory(
                name="Workday time",
                parameter=ActivationRule.Parameter.TIME.value,
                operator=ActivationRule.Operator.BETWEEN.value,
                value=["09:00:00", "21:00:00"],
            ),
            ActivationRuleFactory(
                name="Workday weekday",
                parameter=ActivationRule.Parameter.WEEKDAY.value,
                operator=ActivationRule.Operator.BETWEEN.value,
                value=[1, 5],
            ),
            ActivationRuleFactory(
                name="Not public holiday",
                parameter=ActivationRule.Parameter.DATE.value,
                operator=ActivationRule.Operator.NOT_IN.value,
                value=HOLIDAYS.keys(),
            ),
        ],
    )

    # METERS AND DEMAND
    meters = TariffGroupFactory(name="Meters")
    TariffFactory(
        supplier=supplier,
        group=meters,
        name="Daily metering charge",
        # TODO: seems like not fixed. Need to clarify dependency
        unit_type=UnitType.FIXED.value,
        unit_price=Decimal("91.65"),
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
