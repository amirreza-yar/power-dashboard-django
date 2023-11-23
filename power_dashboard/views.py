from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as filters
import datetime
from .serializers import UserSerializer, GroupSerializer, PowerMeterSerializer
from .models import PowerMeter
from .filters import PowerMeterCurretFilter, PowerMeterDateFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permissions_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permissions_classes = [permissions.IsAuthenticated]

# class PowerMeterViewSet(viewsets.ModelViewSet):
#     queryset = PowerMeter.objects.all()
#     serializer_class = PowerMeterSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_class = PowerMeterDateFilter

#     # filterset_fields = ['datetime']

#     permission_classes = []

#     @action(detail=False, methods=['get'], url_path=r"add-power")
#     def add_data(self, request, *args, **kwargs):
#         print("Create called!")
        
#         # Extract parameters from the query string
#         current = request.GET.get('current')
#         datetime_str = request.GET.get('datetime')

#         if current is not None and datetime_str is not None:
#             # Convert datetime string to a datetime object
#             datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')

#             # Create a new PowerMeter instance
#             power_meter = PowerMeter.objects.create(current=current, datetime=datetime_obj)

#             # Serialize the created instance
#             serializer = PowerMeterSerializer(power_meter)

#             # Return a successful response
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         # If 'current' or 'datetime' parameters are not provided, return a bad request response
#         return Response({'error': 'Please provide both current and datetime parameters in the query string.'}, status=status.HTTP_400_BAD_REQUEST)

class PowerMeterViewSet(viewsets.ModelViewSet):
    queryset = PowerMeter.objects.all()
    serializer_class = PowerMeterSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PowerMeterDateFilter
    permission_classes = ()
    http_method_names = ['get', ]

    @action(detail=False, methods=["get"], url_path=r'add-data',)
    def add_data(self, request):
        print("ADD_DATA called!")
        current = request.GET.get('current')
        datetime_str = request.GET.get('datetime')
        print("current and datetime:", current, datetime_str, sep=", ")
        if current is not None and datetime_str is not None:
            # Convert datetime string to a datetime object
            datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')

            # Create a new PowerMeter instance
            power_meter = PowerMeter.objects.create(current=current, datetime=datetime_obj)

            # Serialize the created instance
            serializer = PowerMeterSerializer(power_meter)

            # Return a successful response
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If 'current' or 'datetime' parameters are not provided, return a bad request response
        return Response({'error': 'Please provide both current and datetime parameters in the query string.'}, status=status.HTTP_400_BAD_REQUEST)