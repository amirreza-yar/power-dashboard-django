from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, PowerMeterViewSet, GroupViewSet, MinMaxPowerViewSet, AvgPowerViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'power', PowerMeterViewSet)
router.register(r'min-max-power', MinMaxPowerViewSet)
router.register(r'avg-power', AvgPowerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]