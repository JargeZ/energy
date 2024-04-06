import logging
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from typing import cast

from django.db.models import QuerySet
from energy.consumption.models import EnergyQuantile
from energy.customers.models import Customer
from energy.suppliers.models import EnergySupplier
from energy.tariffs.models import UnitType, Tariff
from energy.tariffs.services.ConsumptionCalculator import schema as s

logger = logging.getLogger(__name__)

class CalculatorService:
    def __init__(
            self, *,
            supplier: EnergySupplier,
            customer: Customer,
            from_date: datetime,
            to_date: datetime,
    ):
        self.supplier = supplier
        self.customer = customer
        self.from_date = from_date
        self.to_date = to_date

        self.total: dict[UnitType, Decimal] = defaultdict(Decimal)
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
        return self.supplier.tariffs.order_by('-priority')

    def _add_quantile(self, quantile: s.Quantile):
        quantile_cost = Decimal(0)
        verify_consumption = Decimal(0)

        by_quantile = self._by_tariff_quantile_consumption(quantile)
        for tariff, consumption in by_quantile.items():
            cost_part = tariff.unit_price * (consumption * tariff.consumption_coefficient)
            self.total_by_tariff[tariff] += cost_part

            logger.info(f"for Q {quantile.start} - {quantile.end} - {quantile.value} using [{tariff.name}] ({tariff.unit_type}x{tariff.unit_price}) X {consumption} = cost: {cost_part}")

            quantile_cost += cost_part
            verify_consumption += consumption

        if verify_consumption % quantile.value:
            raise ValueError('Consumption mismatch not all consumption was calculated')

        # TODO: add by tariff total
        self.total[UnitType(quantile.type).value] += quantile_cost

    def calculate_total(self) -> Decimal:
        TARIFF_FIRST_HANDLERS = {
            UnitType.DAYS.value: self._eval_tariff_type_days,
            UnitType.FIXED.value: self._eval_tariff_type_fixed,
        }

        tariff_first_tariffs: QuerySet[Tariff] = self._get_tariffs().filter(
            unit_type__in=TARIFF_FIRST_HANDLERS.keys()
        )
        for tariff in tariff_first_tariffs:
            tariff_type = UnitType(tariff.unit_type).value
            TARIFF_FIRST_HANDLERS[tariff_type](tariff)

        for consumption_quantile in self._get_quantiles(self.from_date, self.to_date):
            domain_quantile = s.Quantile.from_consumption(consumption_quantile, self.from_date, self.to_date)
            self._add_quantile(domain_quantile)

        return cast(Decimal, sum(self.total.values()))

    def _eval_tariff_type_days(self, tariff: Tariff):
        days = (self.to_date - self.from_date).days
        cost = tariff.unit_price * days
        self.total[UnitType.DAYS.value] += cost
        self.total_by_tariff[tariff] += cost

    def _eval_tariff_type_fixed(self, tariff: Tariff):
        pass

    def _get_matching_tariffs(self, quantile: s.Quantile) -> list[Tariff]:
        matching_tariffs = []
        all_tariffs = self._get_tariffs().prefetch_related('condition').filter(unit_type=quantile.type.value)

        for t in all_tariffs:
            assert t.condition

            if t.condition and t.condition.is_match(quantile.start, quantile.end):
                matching_tariffs.append(t)

            if not t.condition:
                matching_tariffs.append(t)

        return matching_tariffs

    def _by_tariff_quantile_consumption(self, quantile: s.Quantile) -> dict[Tariff, Decimal]:
        matching_tariffs = self._get_matching_tariffs(quantile)
        groups = [t.group_id for t in matching_tariffs]
        if len(groups) != len(set(groups)):
            # TODO: implement multiple matching tariffs
            raise NotImplementedError('Multiple tariffs from the same group found')

        if len(matching_tariffs) == 0:
            raise ValueError('No matching tariffs found')

        return {t: quantile.value for t in matching_tariffs}
