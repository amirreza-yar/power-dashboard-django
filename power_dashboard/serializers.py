from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import PowerMeter, CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'email', 'groups', 'uuid']
        extra_kwargs = {
            # This tells DRF to use 'uuid' as the lookup field
            'url': {'lookup_field': 'uuid'}
        }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PowerMeterSerializer(serializers.ModelSerializer):

    user_uuid = serializers.ReadOnlyField(source='user.uuid')

    class Meta:
        model = PowerMeter
        fields = ['power', 'datetime', 'current', 'voltage', 'user_uuid']


class HourlyPowerSerializer(serializers.Serializer):
    power = serializers.FloatField()
    hour = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')


class DailyStatSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    min_power = serializers.FloatField()
    max_power = serializers.FloatField()
    avg_power = serializers.FloatField()
    # powers = HourlyPowerSerializer(many=True)

    class Meta:
        model = PowerMeter
        fields = ['date', 'min_power', 'max_power', 'avg_power']


class MinMaxPowerSerializer(serializers.ModelSerializer):
    min_power = serializers.FloatField()
    max_power = serializers.FloatField()

    class Meta:
        model = PowerMeter
        fields = ['power', 'date', 'min_power', 'max_power']


class AvgPowerSerializer(serializers.ModelSerializer):
    avg_power = serializers.FloatField()

    class Meta:
        model = PowerMeter
        fields = ['avg_power', 'date', 'datetime', 'hour']
