from .settings import *  # noqa
from .settings import DATABASES

# Here you can override any setting from settings.py file if you need it for tests

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
