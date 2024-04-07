from django.contrib import admin
from energy.consumption.models import EnergyConsumptionRecord


@admin.register(EnergyConsumptionRecord)
class EnergyConsumptionRecordAdmin(admin.ModelAdmin):
    list_display = (
        "start",
        "end",
        "customer",
        "type",
        "value",
    )
    list_filter = (
        "start",
        "end",
        "customer",
        "type"
    )
    search_fields = ("customer__business_name",)
    ordering = ("start",)
