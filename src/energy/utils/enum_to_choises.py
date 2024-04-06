from enum import Enum

from django.utils.functional import classproperty


class EnumChoiceMixin(Enum):
    @classproperty
    def choices(cls):
        return [(item.value, item.name.lower().replace("_", " ").capitalize()) for item in cls]  # type: ignore
