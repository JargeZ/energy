from energy.tariffs.models import ActivationRule, Tariff
from energy.tariffs.schema.activation_condition.base import BaseConditionRuleHandler
from energy.tariffs.schema.activation_condition.factory import PARAMETER_HANDLERS
from energy.tariffs.services.ConsumptionCalculator import Calculator
from energy.tariffs.services.ConsumptionCalculator.schema import Quantile


class TariffMatcherService:
    rules: list[BaseConditionRuleHandler]

    def __init__(self, tariff: Tariff):
        self.tariff = tariff
        self.rules = []

        rule: ActivationRule
        for rule in tariff.activation_rules.all():
            parameter: ActivationRule.Parameter = ActivationRule.Parameter(rule.parameter)
            rule_handler_class = PARAMETER_HANDLERS[parameter]
            self.rules.append(rule_handler_class(rule=rule, tariff=self.tariff))

    def is_match(self, quantile: Quantile, calculator: Calculator) -> bool:
        if quantile.type != self.tariff.unit_type:
            return False

        if len(self.rules) == 0:
            return True

        return all([rule.is_match(quantile, calculator) for rule in self.rules])
