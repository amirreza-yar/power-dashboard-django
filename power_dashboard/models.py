from django.db import models
from django.utils import timezone
from django.db.models import Min, Max


class PowerMeter(models.Model):
    current = models.FloatField()
    voltage = models.FloatField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

    @property
    def power(self):
        return float(self.current) * float(self.voltage) * 0.9

    @property
    def date(self):
        return self.datetime.date()

    def __str__(self):
        return f"{round(self.power, 2)}W at {self.datetime}"