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
        fields = "__all__"

