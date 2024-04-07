from enum import Enum

from django.utils.functional import classproperty


class EnumChoiceMixin(Enum):
    @classproperty
    def choices(cls):
        return [(item.value, item.name.lower().replace("_", " ").capitalize()) for item in cls]  # type: ignore

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other

        return self.value == other.consumption_value

    def __hash__(self):
        return hash(self.value)
