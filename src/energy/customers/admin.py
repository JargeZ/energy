import logging

from django.contrib import admin
from django.utils.safestring import mark_safe
from energy.consumption.services.BillPrinter.plain_text_printer import PlainTextBillPrinter
from energy.customers.models import Customer, DEMO_FROM_DATE, DEMO_TO_DATE
from energy.suppliers.models import EnergySupplier
from energy.tariffs.services.ConsumptionCalculator.Calculator import CalculatorService

logger = logging.getLogger(__name__)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "email",
        "phone",
        "address",
    )
    search_fields = ("business_name",)
    ordering = ("business_name",)
    readonly_fields = ["calc_for_all_suppliers"]

    def calc_for_all_suppliers(self, obj: Customer):
        summary = "Calculation for all suppliers\n\n"
        for supplier in EnergySupplier.objects.all():
            calculator = CalculatorService(
                supplier=supplier,
                customer=obj,
                from_date=obj.demo_bill_from.astimezone(obj.time_zone) or DEMO_FROM_DATE,
                to_date=obj.demo_bill_to.astimezone(obj.time_zone) or DEMO_TO_DATE,
            )
            try:
                calculator.calculate_total()
                render = PlainTextBillPrinter(calculator).render()
                summary += f"\n---\nBill for {supplier.name} calculated\n{render}"
            except Exception as e:
                summary += f"\n\nError calculating bill for {supplier.name}\n"
                logger.exception(e)
                continue

        return mark_safe(f"<pre>{summary}</pre>")
