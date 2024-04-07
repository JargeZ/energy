from django.contrib import admin
from energy.tariffs.models import ActivationRule, TariffGroup, Tariff
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


@admin.register(TariffGroup)
class TariffGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivationRule)
class ActivationRuleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parameter",
        "operator",
        "value",
    )
    list_filter = (
        "parameter",
        "operator",
    )
    search_fields = (
        "name",
        "parameter",
        "value",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group",
        "unit_type",
        "unit_price",
    )
    search_fields = (
        "supplier__name",
        "name",
        "unit_type",
    )
    list_filter = (
        "group",
        "unit_type",
        "supplier",
    )
