from decimal import Decimal


def exclude_gst(price: Decimal) -> Decimal:
    return price / Decimal(11) * Decimal(10)
