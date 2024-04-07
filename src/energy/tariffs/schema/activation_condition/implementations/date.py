from energy.tariffs.schema.activation_condition.base import BaseConditionRuleHandler
from energy.tariffs.services.ConsumptionCalculator import Calculator
from energy.tariffs.services.ConsumptionCalculator.schema import Quantile


class DateRule(BaseConditionRuleHandler):
    def check_eq(self, quantile: Quantile, calculator: Calculator) -> bool:
        date_part = quantile.date.date()
        return self.condition_value == date_part

    def check_in(self, quantile: Quantile, calculator: Calculator) -> bool:
        date_part = quantile.date.date()
        return date_part in self.condition_value

    def check_between(self, quantile: Quantile, calculator: Calculator) -> bool:
        date_part = quantile.date.date()
        return self.condition_value[0] <= date_part <= self.condition_value[1]
