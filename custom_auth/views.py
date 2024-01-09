from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

# class UUIDTokenObtainSerializer(TokenObtainPairSerializer):

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = CustomUser.UUID_FIELD
    uuid = serializers.UUIDField()
    password = serializers.CharField(write_only=True)

    default_error_messages = {
        'no_active_account': 'No active account found with the given UUID.',
        'invalid_credentials': 'Unable to log in with provided credentials.',
    }

    def validate(self, attrs):
        uuid = attrs.get("uuid")
        password = attrs.get("password")

        if uuid and password:
            try:
                user = CustomUser.objects.get(uuid=uuid)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(self.default_error_messages['no_active_account'])
            
            if user.check_password(password):
                if not user.is_active:
                    raise serializers.ValidationError(self.default_error_messages['no_active_account'])

                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return data
            else:
                raise serializers.ValidationError(self.default_error_messages['invalid_credentials'])

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenObtainPairSerializer