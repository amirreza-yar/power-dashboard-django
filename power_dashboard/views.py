from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as filters
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

class PowerMeterViewSet(viewsets.ModelViewSet):
    queryset = PowerMeter.objects.all()
    serializer_class = PowerMeterSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PowerMeterDateFilter

    # filterset_fields = ['datetime']

    permission_classes = []


# class PowerMeterViewSet(APIView):
#     def get(self, request, format=None, date=None):
#         powers = PowerMeter.objects.all()
#         if date:
#             serializer = PowerMeterSerializer(powers, many=True)
#             return Response(serializer.data)
            
#         return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)