from django.contrib import admin
from energy.suppliers.models import EnergySupplier
from energy.tariffs.models import Tariff


class TariffInline(admin.StackedInline):
    model = Tariff


@admin.register(EnergySupplier)
class EnergySupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    search_fields = ("name",)
    inlines = [TariffInline]
