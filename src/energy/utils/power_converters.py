from decimal import Decimal

POWER_FACTOR = Decimal("0.8")


def kVA_to_kW(kVA: Decimal, power_factor: Decimal = POWER_FACTOR) -> Decimal:
    return kVA * power_factor


def kW_to_kVA(kW: Decimal, power_factor: Decimal = POWER_FACTOR) -> Decimal:
    return kW / power_factor
