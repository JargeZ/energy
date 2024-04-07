import abc
from typing import Any

from energy.tariffs.services.ConsumptionCalculator.Calculator import CalculatorService


class BaseBillPrinter(abc.ABC):
    def __init__(self, calculator: CalculatorService):
        self.calculator = calculator

    @abc.abstractmethod
    def render(self) -> Any:
        raise NotImplementedError()
