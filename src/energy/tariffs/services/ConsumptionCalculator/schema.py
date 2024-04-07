from datetime import datetime, timedelta
from decimal import Decimal
from typing import Generator

from pydantic import BaseModel, ConfigDict

from energy.consumption.models import EnergyConsumptionRecord
from energy.tariffs.models import EnergyType


class Quantile(BaseModel):
    consumption_value: Decimal
    type: EnergyType

    date: datetime
    length: timedelta

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class QuantileRange(BaseModel):
    value: Decimal
    type: EnergyType

    start: datetime
    end: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_consumption(cls, consumption: EnergyConsumptionRecord, from_date: datetime, to_date: datetime):
        value = consumption.value
        start = consumption.start.astimezone(from_date.tzinfo)
        end = consumption.end.astimezone(from_date.tzinfo)

        if consumption.start < from_date:
            diff = consumption.start - from_date
            proportion = diff / (consumption.end - consumption.start)
            value = consumption.value * proportion
            start = from_date

        if consumption.end > to_date:
            diff = to_date - consumption.end
            proportion = diff / (consumption.end - consumption.start)
            value = consumption.value * proportion
            end = to_date

        return cls(
            value=value,
            type=EnergyType(consumption.type),
            start=start,
            end=end,
        )

    def by_quantiles(self, quantile_size: timedelta) -> Generator[Quantile, None, None]:
        current_slice = self.start
        diff = self.end - self.start
        if diff % quantile_size:
            # partial is not suported yet
            raise ValueError(f"Quantile {self} size should be a divided of the {quantile_size}")

        count = diff // quantile_size
        each_consumption_value = self.value / count

        while current_slice < self.end:
            yield Quantile(
                consumption_value=each_consumption_value,
                type=self.type,
                date=current_slice,
                length=quantile_size,
            )
            current_slice += quantile_size
