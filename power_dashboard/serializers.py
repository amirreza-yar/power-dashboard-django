from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import PowerMeter


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PowerMeterSerializer(serializers.ModelSerializer):

    class Meta:
        model = PowerMeter
        fields = ['power', 'datetime',]


class MinMaxPowerSerializer(serializers.ModelSerializer):
    min_power = serializers.FloatField()
    max_power = serializers.FloatField()

    class Meta:
        model = PowerMeter
        fields = ['power', 'date', 'min_power', 'max_power']
