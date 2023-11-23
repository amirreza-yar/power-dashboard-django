import django_filters
from django_filters import rest_framework as filters
from django.utils import timezone
from .models import PowerMeter

class PowerMeterDateFilter(django_filters.FilterSet):
    # date = django_filters.CharFilter(method='filter_by_date')

    date = django_filters.CharFilter(
        field_name='datetime', method='filter_by_date', label="Dates to be filtered")

    def filter_by_date(self, queryset, name, value):
        today = timezone.now().date()
        if value == 'today':
            # print("?date=today called!")
            return queryset.filter(datetime__date=today)
        elif value == 'yesterday':
            yesterday = today - timezone.timedelta(days=1)
            return queryset.filter(datetime__date=yesterday)
        elif value == 'last7days':
            seven_days_ago = today - timezone.timedelta(days=7)
            return queryset.filter(datetime__date__gte=seven_days_ago)
        else:
            # You can handle additional cases or default behavior here
            return queryset

    class Meta:
        model = PowerMeter
        fields = ['datetime']

class PowerMeterCurretFilter(filters.FilterSet):
    min_power = filters.NumberFilter(field_name="current", lookup_expr='gte')
    max_power = filters.NumberFilter(field_name="current", lookup_expr='lte')

    class Meta:
        model = PowerMeter
        fields = ['current',]

class PowerMeterCurretFilter(filters.FilterSet):
    min_power = filters.NumberFilter(field_name="current", lookup_expr='gte')
    max_power = filters.NumberFilter(field_name="current", lookup_expr='lte')

    class Meta:
        model = PowerMeter
        fields = ['current',]