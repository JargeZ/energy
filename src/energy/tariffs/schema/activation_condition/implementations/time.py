from typing import TYPE_CHECKING

from energy.tariffs.schema.activation_condition.base import BaseConditionRuleHandler
from energy.tariffs.services.ConsumptionCalculator.schema import Quantile

if TYPE_CHECKING:
    from energy.tariffs.services.ConsumptionCalculator.Calculator import (
        CalculatorService,
    )


class TimeRule(BaseConditionRuleHandler):
    def check_eq(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        time_part = quantile.date.time()
        return self.condition_value == time_part

    def check_in(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        time_part = quantile.date.time()
        return time_part in self.condition_value

    def check_between(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        time_part = quantile.date.time()
        return self.condition_value.root[0] <= time_part <= self.condition_value.root[1]
