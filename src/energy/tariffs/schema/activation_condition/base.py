import abc
from abc import abstractmethod
from typing import TYPE_CHECKING

from energy.tariffs.models import ActivationRule, ConditionValue, Tariff
from energy.tariffs.services.ConsumptionCalculator import schema as s

if TYPE_CHECKING:
    from energy.tariffs.services.ConsumptionCalculator.Calculator import (
        CalculatorService,
    )


class BaseConditionRuleHandler(abc.ABC):
    def __init__(self, rule: ActivationRule, tariff: Tariff):
        self.rule = rule
        self.condition_value: ConditionValue = rule.value
        self.tariff = tariff

    # EQ = "eq"
    # IN = "in"
    # NOT_IN = "not_in"
    # BETWEEN = "between"
    # NOT_BETWEEN = "not_between"

    @abstractmethod
    def check_eq(self, quantile: s.Quantile, calculator: "CalculatorService") -> bool:
        raise NotImplementedError()

    @abstractmethod
    def check_in(self, quantile: s.Quantile, calculator: "CalculatorService") -> bool:
        raise NotImplementedError()

    def check_not_in(self, quantile: s.Quantile, calculator: "CalculatorService") -> bool:
        return not self.check_in(quantile, calculator)

    @abstractmethod
    def check_between(self, quantile: s.Quantile, calculator: "CalculatorService") -> bool:
        raise NotImplementedError()

    def check_not_between(self, quantile: s.Quantile, calculator: "CalculatorService") -> bool:
        return not self.check_between(quantile, calculator)

    def is_match(self, quantile: s.Quantile, calculator: "CalculatorService") -> bool:
        postfix = self.rule.operator.value
        method_name = f"check_{postfix}"
        method = getattr(self, method_name)
        return method(quantile)
