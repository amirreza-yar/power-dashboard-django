from django.contrib.auth.models import Group
from django.db.models.functions import TruncHour
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as filters
import datetime
import jdatetime
import pandas
from pathlib import Path
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, GroupSerializer, PowerMeterSerializer, MinMaxPowerSerializer, AvgPowerSerializer, DailyStatSerializer, PowerMeterExportSerializer
from .models import PowerMeter, CustomUser
from .filters import PowerMeterDateFilter, MinMaxPowerDateFilter, AvgPowerDateFilter, DailyStatFilter
from rest_framework_csv.renderers import CSVRenderer
from datetime import timedelta
from django.http import JsonResponse
from django.db.models import Min, Max, Avg, ExpressionWrapper, F, FloatField


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'uuid'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class RealTimeViewSet(viewsets.ModelViewSet):
    queryset = PowerMeter.objects.all().order_by('-datetime')
    serializer_class = PowerMeterSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get',]

    def list(self, request, *args, **kwargs):
        # Assuming the date is passed as a query parameter
        try:
            queryset = self.get_queryset()

            # Compute min and max power for the specific day

            avg_power = queryset.aggregate(
                max_power=Avg(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()
                ))
            )['max_power']

            print([{'power': entry.power, 'hour': entry.datetime}
                  for entry in queryset])
            # Return the results as a JSON response
            data = {
                'avg_power': avg_power,
                'powers': [{'power': entry.power, 'hour': entry.datetime} for entry in queryset[:40]],
            }
            return JsonResponse(data)

        except (ValueError, TypeError):
            # Handle invalid date format or missing date parameter
            return JsonResponse({
                'avg_power': None,
                'powers': None,
            }, status=200)


class EnergyStatViewSet(viewsets.ModelViewSet):
    queryset = PowerMeter.objects.all().order_by('datetime')
    serializer_class = DailyStatSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = DailyStatFilter
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', ]

    def list(self, request, *args, **kwargs):
        # Get the input date range (last7days, last14days, last30days)
        input_range = request.query_params.get('range')

        # Determine the start date based on the input range
        today = datetime.date.today()
        if input_range == 'last7days':
            start_date = today - timedelta(days=7)
        elif input_range == 'last14days':
            start_date = today - timedelta(days=14)
        elif input_range == 'last30days':
            start_date = today - timedelta(days=30)
        else:
            # Handle invalid input range
            return JsonResponse({
                'error': 'Invalid input range.'
            }, status=400)

        # Filter records within the specified date range
        queryset = self.get_queryset().filter(
            datetime__date__gte=start_date, datetime__date__lte=today)

        # Compute energies for each day within the range
        energy_data = {}
        for date in (start_date + timedelta(n) for n in range((today - start_date).days + 1)):
            daily_queryset = queryset.filter(datetime__date=date)
            hourly_powers = daily_queryset.values(
                hour=TruncHour('datetime')
            ).annotate(
                power=Avg(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()
                ))
            ).order_by('hour')

            hourly_energies = []
            for i in range(len(hourly_powers) - 1):
                energy = ((hourly_powers[i]['power'] +
                           hourly_powers[i + 1]['power']) / 2) * 1
                hourly_energies.append(energy)

            total_energy = sum(hourly_energies)
            energy_data[date.strftime('%Y-%m-%d')] = total_energy

        # Return the energies for each day within the range
        return JsonResponse(energy_data)


class DailyStatViewSet(viewsets.ModelViewSet):
    queryset = PowerMeter.objects.all().order_by('datetime')
    serializer_class = DailyStatSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = DailyStatFilter
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', ]

    def list(self, request, *args, **kwargs):
        # Assuming the date is passed as a query parameter
        date_str = request.query_params.get('date')
        try:
            # Parse the input date string to a datetime object
            input_date = datetime.datetime.strptime(
                date_str, '%Y-%m-%d').date()

            # Filter records for the specific day
            queryset = self.get_queryset().filter(datetime__date=input_date)

            # Compute min and max power for the specific day
            min_power = queryset.aggregate(
                min_power=Min(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()
                ))
            )['min_power']

            max_power = queryset.aggregate(
                max_power=Max(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()
                ))
            )['max_power']

            avg_power = queryset.aggregate(
                max_power=Avg(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()
                ))
            )['max_power']

            hourly_powers = queryset.values(
                hour=TruncHour('datetime')
            ).annotate(
                power=Avg(ExpressionWrapper(
                    F('current') * 220 * 0.9, output_field=FloatField()
                ))
            ).order_by('hour')

            hourly_energies = []
            for i in range(len(hourly_powers) - 1):
                # Assuming a 1-hour time interval
                energy = ((hourly_powers[i]['power'] +
                          hourly_powers[i + 1]['power']) / 2) * 1
                hourly_energies.append(energy)

            # Compute the total energy consumption for the day
            total_energy = sum(hourly_energies)

            # Return the results as a JSON response
            if min_power is not None and max_power is not None:
                data = {
                    'date': input_date.strftime('%Y-%m-%d'),
                    'min_power': min_power,
                    'max_power': max_power,
                    'avg_power': avg_power,
                    'energy': total_energy,
                    'powers': [{'power': entry['power'], 'hour': entry['hour'].strftime('%Y-%m-%dT%H:%M:%S')} for entry in hourly_powers]
                }
                return JsonResponse(data)
            else:
                return JsonResponse({
                    'date': None,
                    'min_power': None,
                    'max_power': None,
                    'avg_power': None,
                    'energy': None,
                    'powers': None,
                }, status=200)

        except (ValueError, TypeError):
            # Handle invalid date format or missing date parameter
            return JsonResponse({
                'date': None,
                'min_power': None,
                'max_power': None,
                'avg_power': None,
                'energy': None,
                'powers': None,
            }, status=200)


class PowerMeterViewSet(viewsets.ModelViewSet):
    queryset = PowerMeter.objects.all().order_by('datetime')
    serializer_class = PowerMeterSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = PowerMeterDateFilter
    # permission_classes = [permissions.IsAuthenticated]
    # http_method_names = ['get', ]

    @action(detail=False, methods=["get"], url_path=r'add',)
    def add_data(self, request):
        # print("ADD_DATA called!")
        current = request.GET.get('current')
        voltage = request.GET.get('voltage')
        datetime_str = request.GET.get('datetime')
        user_uuid = request.GET.get('uuid')
        print(user_uuid)
        # print("current and datetime:", current, datetime_str, sep=", ")
        if current is not None and datetime_str is not None and user_uuid is not None:
            # Convert datetime string to a datetime object

            try:

                user = CustomUser.objects.get(uuid=user_uuid)
                datetime_obj = datetime.datetime.strptime(
                    datetime_str, '%Y-%m-%dT%H:%M:%S')

                # "current / 2" --> Yousef Niazi requested
                power_meter = PowerMeter.objects.create(
                    current=float(current) / 2, voltage=voltage, datetime=datetime_obj, user=user)

                serializer = PowerMeterSerializer(power_meter)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                Response({'error': 'User does not exists.'},
                         status=status.HTTP_400_BAD_REQUEST)

        # If 'current' or 'datetime' parameters are not provided, return a bad request response
        return Response({'error': 'Please provide both current, datetime and uuid parameters in the query string.'}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=["get"], url_path=r'developer_add',)
    # def add_data(self, request):
    #     try:
    #         password = request.GET.get('pass')
    #         if password == "*987412365Yar":
    #             FILE_PATH = Path(__file__).resolve().parent.parent
    #             print(FILE_PATH / 'power_data.csv')

    #             csv_file_path = FILE_PATH / 'power_data.csv'
    #             df = pandas.read_csv(csv_file_path, header=None)

    #             dates = list(df.iloc[0:, 0])
    #             times = list(df.iloc[0, 0:])

    #             counter = 0

    #             for date in range(1, len(dates)):
    #                 for time in range(1, len(times)):
    #                     datetime_str = f"{dates[date]}T{times[time]}"
    #                     current = df.iloc[date, time]
    #                     counter += 1

    #                     datetime_obj = datetime.datetime.strptime(
    #                         datetime_str, '%Y-%m-%dT%H:%M:%S')

    #                     # Create a new PowerMeter instance
    #                     power_meter = PowerMeter.objects.create(
    #                         current=current, datetime=datetime_obj)

    #                     print(f"Power created: {power_meter}")

    #             return Response({"ok", True}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"ok", False}, status=status.HTTP_400_BAD_REQUEST)
    #     except:
    #         return Response({"ok", False}, status=status.HTTP_403_FORBIDDEN)


class MinMaxPowerViewSet(viewsets.ModelViewSet):
    queryset = PowerMeter.objects.all()
    serializer_class = MinMaxPowerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MinMaxPowerDateFilter
    permission_classes = ()
    http_method_names = ['get', ]


class AvgPowerViewSet(viewsets.ModelViewSet):
    queryset = PowerMeter.objects.all()
    serializer_class = AvgPowerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AvgPowerDateFilter
    permission_classes = ()
    http_method_names = ['get', ]


class PowerMeterCSVExportAPIView(APIView):
    renderer_classes = [CSVRenderer]
    csv_filename = 'custom_filename.csv'

    def get(self, request, *args, **kwargs):
        queryset = PowerMeter.objects.all()
        value = request.GET.get('date')
        try:
            # Parse the input date string to a datetime object
            input_date = datetime.datetime.strptime(
                value, '%Y-%m-%d').date()
            # Filter records for the specified date
            filtered_queryset = queryset.filter(
                datetime__date=input_date).order_by('datetime')
            serializer = PowerMeterExportSerializer(
                filtered_queryset, many=True)
            return Response(serializer.data)
        except ValueError:
            return queryset.none()

    def finalize_response(self, request, response, *args, **kwargs):
        date = request.GET.get('date')
        input_date = datetime.datetime.strptime(
                date, '%Y-%m-%d').date()
        jalali_date = jdatetime.date.fromgregorian(date=input_date)

        response['Content-Disposition'] = f'attachment; filename="{str(jalali_date)}_full_data.csv"'
        return super().finalize_response(request, response, *args, **kwargs)
    

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
