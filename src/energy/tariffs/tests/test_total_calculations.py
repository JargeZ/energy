import datetime
from zoneinfo import ZoneInfo

from energy.tariffs.services.ConsumptionCalculator.Calculator import CalculatorService
from energy.tests.BaseEnergyTest import BaseEnergyTest


class TestTotalCalculations(BaseEnergyTest):
    def test_blue_supplier_set_total(self, blue_supplier, blue_customer):
        EXPECTED_TOTAL_BLUE = 46.71 + 215.85 + 564.63 + 148.63 + 101.93 + 171.47 + 288.66 + 536.31
        FROM_DATE = datetime.datetime(2024, 1, 1, tzinfo=ZoneInfo("Australia/Sydney"))
        TO_DATE = datetime.datetime(2024, 1, 31, tzinfo=ZoneInfo("Australia/Sydney")) + datetime.timedelta(days=1)

        calculator = CalculatorService(
            supplier=blue_supplier,
            customer=blue_customer
        )

        assert calculator.calculate_total(from_date=FROM_DATE, to_date=TO_DATE) == EXPECTED_TOTAL_BLUE
