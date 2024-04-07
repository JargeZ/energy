# Generated by Django 5.0.4 on 2024-04-07 11:10

import timezone_field.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0002_customer_demo_bill_from_customer_demo_bill_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="time_zone",
            field=timezone_field.fields.TimeZoneField(default="Australia/Sydney", verbose_name="Timezone"),
        ),
    ]