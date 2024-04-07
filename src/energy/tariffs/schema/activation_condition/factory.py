from typing import Type

from energy.tariffs.models import ActivationRule
from energy.tariffs.schema.activation_condition.base import BaseConditionRuleHandler
from energy.tariffs.schema.activation_condition.implementations.consumed_value import (
    ConsumedValueRule,
)
from energy.tariffs.schema.activation_condition.implementations.date import DateRule
from energy.tariffs.schema.activation_condition.implementations.time import TimeRule
from energy.tariffs.schema.activation_condition.implementations.weekday import (
    WeekdayRule,
)

PARAMETER_HANDLERS: dict[ActivationRule.Parameter, Type[BaseConditionRuleHandler]] = {
    ActivationRule.Parameter.DATE: DateRule,
    ActivationRule.Parameter.TIME: TimeRule,
    ActivationRule.Parameter.WEEKDAY: WeekdayRule,
    ActivationRule.Parameter.CONSUMED: ConsumedValueRule,
}
