import decimal
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
from functools import cached_property
from typing import NewType, cast

from django.db.models import QuerySet

from energy.consumption.models import EnergyQuantile
from energy.customers.models import Customer
from energy.suppliers.models import EnergySupplier
from energy.tariffs.models import Tariff, UnitType
from energy.tariffs.services.ConsumptionCalculator import schema as s
from energy.tariffs.services.TariffMatcher.TariffMatcher import TariffMatcherService

decimal.getcontext().prec = 28
logger = logging.getLogger(__name__)
GroupId = NewType("GroupId", int)

# i realize that it would be better to change approach
# if we make every tariff like Accumulator for counted charges
#  so we can "feed" all quantiles to all tariffs and implement
#  comprehensive activation logic for each tariff

# also may be better to split all complete consumption
# records on fixed size quantiles (better vary)
# and "feed" them to tariffs accumulators

# many tariffs can be activated but only first by priority will be used

# TariffCondition goes turn into ActivationRule where we can configure
# every parameter with operators
# EQ, NE, GT, LT, GTE, LTE, IN, NOT_IN, RANGE, NOT_RANGE ...

QUANTILE_SIZE = timedelta(minutes=1)


class CalculatorService:
    total_by_tariff: dict[Tariff, Decimal]

    def __init__(
        self,
        *,
        supplier: EnergySupplier,
        customer: Customer,
        from_date: datetime,
        to_date: datetime,
    ):
        self.supplier = supplier
        self.customer = customer
        self.from_date = from_date
        self.to_date = to_date

        self.total_by_tariff: dict[Tariff, Decimal] = defaultdict(Decimal)

    def _get_quantiles(self, from_date: datetime, to_date: datetime) -> QuerySet[EnergyQuantile]:
        # It covers overlapping periods
        # when quantile starts before <from_date> but ends after <from_date>
        # further, we have to normalize it to overlaps period proportionally
        return self.customer.energy_quantiles.filter(
            end__gte=from_date,
            start__lte=to_date,
        )

    def _get_tariffs(self) -> QuerySet[Tariff]:
        return self.supplier.tariffs.order_by("-priority")

    def _add_range(self, q_range: s.QuantileRange):
        verify_consumption = Decimal(0)

        for q in q_range.by_quantiles(QUANTILE_SIZE):
            by_tariff_consumption = self._by_tariff_quantile_consumption(quantile=q)

            for tariff, consumption in by_tariff_consumption.items():
                cost_part = tariff.unit_price * (consumption * tariff.consumption_coefficient)

                logger.debug(
                    f"for Q {q.date} - {q.consumption_value}/{q_range.value} using "
                    f"[{tariff.name}] ({tariff.unit_type}x{tariff.unit_price}) "
                    f"X {consumption} = cost: {cost_part}"
                )

                self.total_by_tariff[tariff] += cost_part

                verify_consumption += consumption

        # if verify_consumption % q_range.value > Decimal("0.0001"):
        #     raise ValueError("Consumption mismatch not all consumption was calculated")

    def calculate_total(self) -> Decimal:
        non_consumption_based_tariffs = {
            UnitType.DAYS.value: self._eval_tariff_type_days,
            UnitType.FIXED.value: self._eval_tariff_type_fixed,
        }

        # Evaluate fixed, total-day-based and other tariffs
        non_consumption_tariffs: QuerySet[Tariff] = self._get_tariffs().filter(
            unit_type__in=non_consumption_based_tariffs.keys()
        )
        for tariff in non_consumption_tariffs:
            tariff_type = UnitType(tariff.unit_type).value
            non_consumption_based_tariffs[tariff_type](tariff)

        # Feed consumption to consumption-based tariffs
        for consumption_quantile in self._get_quantiles(self.from_date, self.to_date):
            domain_quantile_range = s.QuantileRange.from_consumption(consumption_quantile, self.from_date, self.to_date)
            self._add_range(domain_quantile_range)

        return cast(Decimal, sum(self.total_by_tariff.values()))

    def _eval_tariff_type_days(self, tariff: Tariff):
        days = (self.to_date - self.from_date).days
        cost = tariff.unit_price * days
        self.total_by_tariff[tariff] += cost

    def _eval_tariff_type_fixed(self, tariff: Tariff):
        self.total_by_tariff[tariff] += tariff.unit_price

    # ONE-TIME cost-ish tariffs loading
    @cached_property
    def _tariffs_by_group_with_priority(self) -> dict[GroupId, list[TariffMatcherService]]:
        tariffs = self._get_tariffs().prefetch_related("activation_rules")

        tariffs_by_group = defaultdict(list)

        for tariff in tariffs:
            matcher = TariffMatcherService(tariff)
            tariffs_by_group[tariff.group_id].append(matcher)

        return tariffs_by_group

    def _get_effective_tariffs(self, quantile: s.Quantile) -> list[Tariff]:
        matching_tariffs = []
        all_tariffs = self._tariffs_by_group_with_priority

        for group_id, tariff_matchers in all_tariffs.items():
            for matcher in tariff_matchers:
                if matcher.is_match(quantile, self):
                    matching_tariffs.append(matcher.tariff)
                    break

        return matching_tariffs

    def _by_tariff_quantile_consumption(self, quantile: s.Quantile) -> dict[Tariff, Decimal]:
        matching_tariffs = self._get_effective_tariffs(quantile)

        # check if we have only one tariff from the same group
        # this code may be redundant but now just in case
        groups = [t.group_id for t in matching_tariffs]
        if len(groups) != len(set(groups)):
            raise ValueError("Only one tariff from the same group should be matched. This code should be unrachable.")

        if len(matching_tariffs) == 0:
            raise ValueError("No matching tariffs found")

        return {t: quantile.consumption_value for t in matching_tariffs}
