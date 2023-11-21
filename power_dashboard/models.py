from django.db import models
from django.utils import timezone

class PowerMeter(models.Model):
    current = models.FloatField()
    datetime = models.DateTimeField(default=timezone.now)