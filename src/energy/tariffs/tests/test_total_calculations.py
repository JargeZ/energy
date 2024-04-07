import datetime
import logging
from decimal import Decimal
from zoneinfo import ZoneInfo

from energy.consumption.services.BillPrinter.plain_text_printer import (
    PlainTextBillPrinter,
)
from energy.tariffs.services.ConsumptionCalculator.Calculator import CalculatorService
from energy.tests.BaseEnergyTest import BaseEnergyTest

logger = logging.getLogger(__name__)


class TestTotalCalculations(BaseEnergyTest):
    def test_blue_supplier_set_total(self, blue_supplier, blue_customer, caplog):
        caplog.set_level(logging.INFO)

        EXPECTED_TOTAL_BLUE = (
            Decimal("46.71")
            + Decimal("215.85")
            + Decimal("564.63")
            + Decimal("148.63")
            + Decimal("101.93")
            + Decimal("171.47")
            + Decimal("288.66")
            + Decimal("536.31")
        )
        FROM_DATE = datetime.datetime(2024, 1, 1, tzinfo=ZoneInfo("Australia/Sydney"))
        TO_DATE = datetime.datetime(2024, 2, 1, tzinfo=ZoneInfo("Australia/Sydney"))

        calculator = CalculatorService(
            supplier=blue_supplier,
            customer=blue_customer,
            from_date=FROM_DATE,
            to_date=TO_DATE,
        )

        total = calculator.calculate_total()

        for tariff, cost in calculator.total_by_tariff_cost.items():
            logger.info(f"{tariff.name}: {cost}")

        delta = abs(total - EXPECTED_TOTAL_BLUE)
        assert delta < Decimal("1")

        assert round(total, 1) == round(EXPECTED_TOTAL_BLUE, 1)

    def test_green_supplier_set_total(self, green_supplier, green_customer, caplog):
        caplog.set_level(logging.INFO)

        EXPECTED_TOTAL_GREEN = Decimal("1904.39")

        FROM_DATE = datetime.datetime(2024, 2, 28, tzinfo=ZoneInfo("Australia/Sydney"))
        TO_DATE = datetime.datetime(2024, 3, 25 + 1, tzinfo=ZoneInfo("Australia/Sydney"))

        calculator = CalculatorService(
            supplier=green_supplier,
            customer=green_customer,
            from_date=FROM_DATE,
            to_date=TO_DATE,
        )

        total = calculator.calculate_total()

        summary = PlainTextBillPrinter(calculator).render()
        logger.info(summary)

        delta = abs(total - EXPECTED_TOTAL_GREEN)
        assert delta < Decimal("1")

        assert round(total, 1) == round(EXPECTED_TOTAL_GREEN, 1)
