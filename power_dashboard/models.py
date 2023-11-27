from django.db import models
from django.utils import timezone
from django.db.models import Min, Max


class PowerMeter(models.Model):
    current = models.FloatField()
    datetime = models.DateTimeField(default=timezone.now)

    @property
    def power(self):
        return float(self.current) * 220 * 0.9

    @property
    def date(self):
        return self.datetime.date()
