from rest_framework import serializers
from apps.account.models import User

from apps.account.users_auth.token import verify_token, refresh_access_token


class LoginByPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):
        if not verify_token(request=self.context["request"], raw_token=token):
            raise serializers.ValidationError("Invalid token")
        return token


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")
