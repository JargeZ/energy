from typing import TYPE_CHECKING

from energy.tariffs.schema.activation_condition.base import BaseConditionRuleHandler
from energy.tariffs.services.ConsumptionCalculator.schema import Quantile

if TYPE_CHECKING:
    from energy.tariffs.services.ConsumptionCalculator.Calculator import (
        CalculatorService,
    )


class WeekdayRule(BaseConditionRuleHandler):
    def check_eq(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        weekday = quantile.date.isoweekday()
        return self.condition_value == weekday

    def check_in(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        weekday = quantile.date.isoweekday()
        return weekday in self.condition_value

    def check_between(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        weekday = quantile.date.isoweekday()
        return self.condition_value.root[0] <= weekday <= self.condition_value.root[1]
