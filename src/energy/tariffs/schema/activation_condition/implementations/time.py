from energy.tariffs.schema.activation_condition.base import BaseConditionRuleHandler
from energy.tariffs.services.ConsumptionCalculator import Calculator
from energy.tariffs.services.ConsumptionCalculator.schema import Quantile


class TimeRule(BaseConditionRuleHandler):
    def check_eq(self, quantile: Quantile, calculator: Calculator) -> bool:
        time_part = quantile.date.time()
        return self.condition_value == time_part

    def check_in(self, quantile: Quantile, calculator: Calculator) -> bool:
        time_part = quantile.date.time()
        return time_part in self.condition_value

    def check_between(self, quantile: Quantile, calculator: Calculator) -> bool:
        time_part = quantile.date.time()
        return self.condition_value[0] <= time_part <= self.condition_value[1]
