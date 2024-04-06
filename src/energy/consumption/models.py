from django.db import models
from django.db.models import CheckConstraint, Q
from energy.tariffs.models import EnergyType


class EnergyQuantile(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)

    start = models.DateTimeField()
    end = models.DateTimeField()

    type = models.CharField(max_length=255, choices=EnergyType.choices)
    value = models.DecimalField(max_digits=10, decimal_places=10)

    class Meta:
        db_table = 'energy_quantile'
        constraints = [
            CheckConstraint(
                check=Q(start__lte=models.F('end')),
                name='start_less_than_or_equal_to_end',
            ),
        ]

    def __str__(self):
        diff = self.end - self.start

        return f'{self.type} {diff}'
