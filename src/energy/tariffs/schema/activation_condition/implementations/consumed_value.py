from typing import TYPE_CHECKING

from energy.tariffs.schema.activation_condition.base import BaseConditionRuleHandler
from energy.tariffs.services.ConsumptionCalculator.schema import Quantile

if TYPE_CHECKING:
    from energy.tariffs.services.ConsumptionCalculator.Calculator import (
        CalculatorService,
    )


class ConsumedValueRule(BaseConditionRuleHandler):
    def check_eq(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        consumed = calculator.total_by_tariff[self.tariff]
        return self.condition_value == consumed

    def check_in(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        consumed = calculator.total_by_tariff[self.tariff]
        return consumed in self.condition_value

    def check_between(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        consumed = calculator.total_by_tariff[self.tariff]
        return self.condition_value.root[0] <= consumed <= self.condition_value.root[1]
