from django.db import models
from django.utils import timezone
from django.db.models import Min, Max
from django.contrib.auth.models import AbstractUser, User
import uuid
import jdatetime

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
        return timezone.localtime(self.datetime).date()
    
    @property
    def jdate(self):
        localized_datetime = timezone.localtime(self.datetime)
        gregorian_date = localized_datetime.date()
        
        jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
        
        return f"{jalali_date.year}-{jalali_date.month}-{jalali_date.day}"

    @property
    def hour(self):
        return str(timezone.localtime(self.datetime).hour) + ":00"

    def __str__(self):
        return f"{round(self.power, 2)}W at {self.datetime}"
