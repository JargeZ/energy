from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from energy.consumption.models import EnergyQuantile
from energy.tariffs.models import EnergyType


class Quantile(BaseModel):
    value: Decimal
    type: EnergyType

    start: datetime
    end: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_consumption(cls, consumption: EnergyQuantile, from_date: datetime, to_date: datetime):
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
