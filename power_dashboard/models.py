from django.db import models
from django.utils import timezone
from django.db.models import Min, Max
from django.contrib.auth.models import AbstractUser, User
import uuid


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)


class PowerMeter(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    current = models.FloatField()
    voltage = models.FloatField(default=220, null=True)
    datetime = models.DateTimeField(default=timezone.now)

    @property
    def power(self):
        return float(self.current) * float(self.voltage) * 0.9

    @property
    def date(self):
        return self.datetime.date()

    @property
    def hour(self):
        return self.datetime.hour()

    def __str__(self):
        return f"{round(self.power, 2)}W at {self.datetime}"
