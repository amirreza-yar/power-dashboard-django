from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, PowerMeterViewSet, GroupViewSet, MinMaxPowerViewSet, AvgPowerViewSet, DailyStatViewSet, EnergyStatViewSet, RealTimeViewSet, PowerMeterCSVExportAPIView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'power', PowerMeterViewSet)
# router.register(r'min-max-power', MinMaxPowerViewSet)
# router.register(r'avg-power', AvgPowerViewSet)
router.register(r'daily-stat', DailyStatViewSet)
router.register(r'energy-stat', EnergyStatViewSet)
router.register(r'realtime', RealTimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('power-export/', PowerMeterCSVExportAPIView.as_view(), name="power-export"),
]