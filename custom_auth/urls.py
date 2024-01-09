from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    # ... other URL patterns
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]