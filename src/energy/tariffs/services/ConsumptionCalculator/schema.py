from datetime import datetime
from decimal import Decimal

from energy.consumption.models import EnergyQuantile
from energy.tariffs.models import EnergyType
from pydantic import BaseModel


class Quantile(BaseModel):
    value: Decimal
    type: EnergyType

    start: datetime
    end: datetime

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_consumption(cls, consumption: EnergyQuantile, from_date: datetime, to_date: datetime):
        value = consumption.value
        start = consumption.start
        end = consumption.end

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
