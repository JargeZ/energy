from typing import TYPE_CHECKING

from energy.tariffs.schema.activation_condition.base import BaseConditionRuleHandler
from energy.tariffs.services.ConsumptionCalculator.schema import Quantile

if TYPE_CHECKING:
    from energy.tariffs.services.ConsumptionCalculator.Calculator import (
        CalculatorService,
    )


class DateRule(BaseConditionRuleHandler):
    def check_eq(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        date_part = quantile.date.date()
        return self.condition_value == date_part

    def check_in(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        date_part = quantile.date.date()
        return date_part in self.condition_value

    def check_between(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        date_part = quantile.date.date()
        return self.condition_value.root[0] <= date_part <= self.condition_value.root[1]
