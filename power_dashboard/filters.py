import django_filters
from django_filters import rest_framework as filters
from django.utils import timezone
from django.db.models import Min, Max, Avg, ExpressionWrapper, F, FloatField
from django.db.models.functions import TruncDate, TruncHour
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
        # else:
            # try:
            #     # Parse the input date string to a datetime object
            #     input_date = datetime.datetime.strptime(
            #         value, '%Y-%m-%d').date()

            #     # Filter records for the specific day
            #     queryset = queryset.filter(
            #         datetime__date=input_date).order_by('datetime')

            #     # Compute overall average power for the specific day
            #     daily_avg = queryset.values(date=TruncDate('datetime')).annotate(
            #         avg_power=Avg(ExpressionWrapper(
            #             F('current') * 220 * 0.9, output_field=FloatField()
            #         ))
            #     )

            #     # Compute min and max power for the specific day
            #     daily_stats = queryset.values(date=TruncDate('datetime')).annotate(
            #         min_power=Min(ExpressionWrapper(
            #             F('current') * 220 * 0.9, output_field=FloatField()
            #         )),
            #         max_power=Max(ExpressionWrapper(
            #             F('current') * 220 * 0.9, output_field=FloatField()
            #         ))
            #     )

            #     print(daily_stats)

            #     # Compute average power for each hour of the specific day
            #     hourly_powers = queryset.values(
            #         hour=TruncHour('datetime')
            #     ).annotate(
            #         power=Avg(ExpressionWrapper(
            #             F('current') * 220 * 0.9, output_field=FloatField()
            #         ))
            #     ).order_by('hour')

            #     # Format the output
            #     output = {
            #         'date': input_date,
            #         'min_power': daily_stats['min_power'],
            #         'max_power': daily_stats['max_power'],
            #         'avg_power': daily_stats['avg_power'],
            #         'powers': [{'power': entry['power'], 'hour': entry['hour']} for entry in hourly_powers]
            #     }

            #     return output

            # except ValueError:
            #     # Handle invalid date format
            #     return None

            try:
                pass
            except:
                pass

    class Meta:
        model = PowerMeter
        fields = ['datetime']


class DailyStatFilter(django_filters.FilterSet):

    date = django_filters.CharFilter(
        field_name='datetime', method='filter_by_date', label="Dates to be filtered")

    def filter_by_date(self, queryset, name, value):

        try:
            today = timezone.localdate()
            # Parse the input date string to a datetime object
            input_date = datetime.datetime.strptime(
                value, '%Y-%m-%d').date()
            query = queryset.filter(datetime__date=input_date)

            daily_stats = query.values(date=TruncDate('datetime')).annotate(
                min_power=Min(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()
                )),
                max_power=Max(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()
                ))
            )

            print(daily_stats)

            min_power = queryset.filter(datetime__date=input_date).aggregate(
                Min('current'))['current__min'] * 220 * 0.9
            max_power = queryset.filter(datetime__date=input_date).aggregate(
                Max('current'))['current__max'] * 220 * 0.9
            avg_power = queryset.filter(datetime__date=input_date).aggregate(
                Avg('current'))['current__avg'] * 220 * 0.9
            output = {
                'date': input_date,
                'min_power': min_power,
                'max_power': max_power,
                'avg_power': avg_power,
                # 'powers': [{'power': entry['power'], 'hour': entry['hour']} for entry in hourly_powers]
            }
            print(output)
            return output
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
        elif value == 'last30days':
            thirty_days_ago = today - timezone.timedelta(days=30)
            return queryset.filter(datetime__date__gte=thirty_days_ago, datetime__date__lte=today).values(date=TruncDate('datetime')).annotate(
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
            try:
                # Parse the input date string to a datetime object
                input_date = datetime.datetime.strptime(
                    value, '%Y-%m-%d').date()
                # Filter records for the specified date
                return queryset.filter(datetime__date=input_date).order_by('datetime').values(date=TruncDate('datetime')).annotate(
                    min_power=Min(ExpressionWrapper(
                        F('current') * 220 * 0.9, output_field=FloatField())),
                    max_power=Max(ExpressionWrapper(
                        F('current') * 220 * 0.9, output_field=FloatField()))
                )
            except ValueError:
                # Handle invalid date format
                return queryset.none()

    class Meta:
        model = PowerMeter
        fields = ['datetime']


class AvgPowerDateFilter(django_filters.FilterSet):

    date = django_filters.CharFilter(
        field_name='datetime', method='filter_by_date', label="Dates to be filtered")

    def filter_by_date(self, queryset, name, value):
        today = timezone.localdate()
        if value == 'today':
            print("today is running!")
            return queryset.filter(
                datetime__date=today  # Filter for the specific day
            ).values(
                hour=TruncHour('datetime')  # Extract hour from datetime
            ).annotate(
                avg_power=Avg(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()
                ))
            )
        if value == 'last7days':
            seven_days_ago = today - timezone.timedelta(days=7)
            return queryset.filter(datetime__date__gte=seven_days_ago, datetime__date__lte=today).values(date=TruncDate('datetime')).annotate(
                avg_power=Avg(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField())),
            )
        elif value == 'last14days':
            fourteen_days_ago = today - timezone.timedelta(days=14)
            return queryset.filter(datetime__date__gte=fourteen_days_ago, datetime__date__lte=today).values(date=TruncDate('datetime')).annotate(
                avg_power=Avg(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField())),
            )

        # TODO This doesnt work correctly! The problem is date.
        elif value == 'last30days':
            thirty_days_ago = today - timezone.timedelta(days=30)
            return queryset.filter(datetime__date__gte=thirty_days_ago, datetime__date__lte=today).values(date=TruncDate('datetime')).annotate(
                avg_power=Avg(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField())),
            )

        elif value == 'lastmonth':
            start_of_last_month = (today.replace(
                day=1) - datetime.timedelta(days=1)).replace(day=1)
            end_of_last_month = today.replace(
                day=1) - datetime.timedelta(days=1)
            return queryset.filter(datetime__date__range=[start_of_last_month, end_of_last_month]).order_by('datetime').values(date=TruncDate('datetime')).annotate(
                avg_power=Avg(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField())),
            )

        else:
            try:
                requested_datetime = timezone.make_aware(
                    datetime.datetime.strptime(value, '%Y-%m-%d'))
                return queryset.filter(
                    datetime__date=requested_datetime  # Filter for the specific day
                ).values(
                    hour=TruncHour('datetime')  # Extract hour from datetime
                ).annotate(
                    avg_power=Avg(ExpressionWrapper(
                        F('current') * 220 * 0.9, output_field=FloatField()
                    ))
                )
            except ValueError:
                # Handle invalid date format
                return queryset.none()

    class Meta:
        model = PowerMeter
        fields = ['datetime']
