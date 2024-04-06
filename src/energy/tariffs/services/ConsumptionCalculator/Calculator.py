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
        cost = Decimal(0)
        verify_consumption = Decimal(0)

        by_quantile = self._by_tariff_quantile_consumption(quantile)
        for tariff, consumption in by_quantile.items():
            cost += tariff.unit_price * consumption
            verify_consumption += consumption

        if quantile.value != verify_consumption:
            raise ValueError('Consumption mismatch')

        # TODO: add by tariff total
        self.total[UnitType(quantile.type)] += cost

    def calculate_total(self) -> Decimal:
        TARIFF_FIRST_HANDLERS = {
            UnitType.DAYS: self._eval_tariff_type_days,
            UnitType.FIXED: self._eval_tariff_type_fixed,
        }

        tariff_first_tariffs: QuerySet[Tariff] = self._get_tariffs().filter(
            type__in=TARIFF_FIRST_HANDLERS.keys()
        )
        for tariff in tariff_first_tariffs:
            tariff_type = UnitType(tariff.unit_type)
            TARIFF_FIRST_HANDLERS[tariff_type](tariff)

        for consumption_quantile in self._get_quantiles(self.from_date, self.to_date):
            domain_quantile = s.Quantile.from_consumption(consumption_quantile, self.from_date, self.to_date)
            self._add_quantile(domain_quantile)

        return cast(Decimal, sum(self.total.values()))

    def _eval_tariff_type_days(self, tariff: Tariff):
        pass

    def _eval_tariff_type_fixed(self, tariff: Tariff):
        pass

    def _get_matching_tariffs(self, quantile: s.Quantile) -> list[Tariff]:
        matching_tariffs = []
        all_tariffs = self._get_tariffs().prefetch_related('condition').filter(type=quantile.type)

        for t in all_tariffs:
            assert t.condition

            if t.condition and t.condition.is_match(quantile.start, quantile.end):
                matching_tariffs.append(t)

            if not t.condition:
                matching_tariffs.append(t)

        return matching_tariffs

    def _by_tariff_quantile_consumption(self, quantile: s.Quantile) -> dict[Tariff, Decimal]:
        matching_tariffs = self._get_matching_tariffs(quantile)
        if len(matching_tariffs) == 1:
            t = matching_tariffs[0]
            return {t: quantile.value}

        # TODO: implement multiple matching tariffs
        raise NotImplementedError()
