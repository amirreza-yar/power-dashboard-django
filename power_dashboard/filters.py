import django_filters
from django_filters import rest_framework as filters
from django.utils import timezone
from django.db.models import Min, Max, ExpressionWrapper, F, FloatField
from django.db.models.functions import TruncDate
import datetime

from .models import PowerMeter
from .serializers import MinMaxPowerSerializer


class PowerMeterDateFilter(django_filters.FilterSet):

    date = django_filters.CharFilter(
        field_name='datetime', method='filter_by_date', label="Dates to be filtered")

    def filter_by_date(self, queryset, name, value):
        today = timezone.localdate()
        
        if value == 'today':
            print("Now is: " + str(today - timezone.timedelta(days=1)))
            return queryset.filter(datetime__date=today).order_by('datetime')
        elif value == 'yesterday':
            yesterday = today - timezone.timedelta(days=1)
            return queryset.filter(datetime__date=yesterday).order_by('datetime')
        elif value == 'last7days':
            seven_days_ago = today - timezone.timedelta(days=7)
            return queryset.filter(datetime__date__gte=seven_days_ago, datetime__date__lte=today).order_by('datetime')
        else:
            try:
                # Parse the input date string to a datetime object
                input_date = datetime.datetime.strptime(
                    value, '%Y-%m-%d').date()
                # Filter records for the specified date
                return queryset.filter(datetime__date=input_date).order_by('datetime')
            except ValueError:
                # Handle invalid date format
                return queryset.none()

    class Meta:
        model = PowerMeter
        fields = ['datetime']


class MinMaxPowerDateFilter(django_filters.FilterSet):

    date = django_filters.CharFilter(
        field_name='datetime', method='filter_by_date', label="Dates to be filtered")

    def filter_by_date(self, queryset, name, value):
        today = timezone.localdate()
        if value == 'last7days':
            seven_days_ago = today - timezone.timedelta(days=7)
            return queryset.filter(datetime__date__gte=seven_days_ago, datetime__date__lte=today).values(date=TruncDate('datetime')).annotate(
                min_power=Min(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField())),
                max_power=Max(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()))
            )
        elif value == 'last14days':
            fourteen_days_ago = today - timezone.timedelta(days=14)
            return queryset.filter(datetime__date__gte=fourteen_days_ago, datetime__date__lte=today).values(date=TruncDate('datetime')).annotate(
                min_power=Min(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField())),
                max_power=Max(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()))
            )

        # TODO This doesnt work correctly! The problem is date.
        elif value == 'thismonth':
            start_of_month = today.replace(day=1)
            return queryset.filter(datetime__date__gte=start_of_month, datetime__date__lte=today).order_by('datetime').values(date=TruncDate('datetime')).annotate(
                min_power=Min(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField())),
                max_power=Max(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()))
            )

        elif value == 'lastmonth':
            start_of_last_month = (today.replace(
                day=1) - datetime.timedelta(days=1)).replace(day=1)
            end_of_last_month = today.replace(
                day=1) - datetime.timedelta(days=1)
            return queryset.filter(datetime__date__range=[start_of_last_month, end_of_last_month]).order_by('datetime').values(date=TruncDate('datetime')).annotate(
                min_power=Min(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField())),
                max_power=Max(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()))
            )

        else:
            return queryset.none()

    class Meta:
        model = PowerMeter
        fields = ['datetime']
