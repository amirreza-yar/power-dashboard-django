from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, GroupSerializer, PowerMeterSerializer
from .models import PowerMeter

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
    permissions_classes = []