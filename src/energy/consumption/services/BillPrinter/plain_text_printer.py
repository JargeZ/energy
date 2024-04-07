from collections import defaultdict

from energy.consumption.services.BillPrinter.base_printer import BaseBillPrinter
from energy.tariffs.models import Tariff, TariffGroup
from energy.tariffs.schema.types import GroupId


class PlainTextBillPrinter(BaseBillPrinter):
    def render(self) -> str:
        by_tariff_cost = self.calculator.total_by_tariff_cost
        by_tariff_consumption = self.calculator.total_by_tariff_consumption

        by_group: dict[GroupId, list[Tariff]] = defaultdict(list)
        for tariff, _ in by_tariff_cost.items():
            by_group[GroupId(tariff.group_id)].append(tariff)

        result: list[str] = []
        for group_id, tariffs in by_group.items():
            group = TariffGroup.objects.get(id=group_id)
            result.append(f"\nGroup {group.name}:")

            for tariff in tariffs:
                consumed = by_tariff_consumption[tariff]
                cost = by_tariff_cost[tariff]
                result.append(
                    f"Tariff {tariff.name}"
                    f"\tpriority {tariff.priority}"
                    f"\t{consumed} {tariff.unit_type}"
                    f"\tx {tariff.unit_price}"
                    f"\t = {cost}"
                )

        result.append(f"\nTotal: {sum(by_tariff_cost.values())}")

        return "\n".join(result)
