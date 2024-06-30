from rest_framework import serializers
from apps.account.models import User

from apps.account.users_auth.token import verify_token, refresh_access_token


class LoginByPasswordSerializer(serializers.Serializer):
    """
    Serializer for handling user login via password. It requires two fields:
    - `username`: The username of the user.
    - `password`: The password of the user.
    """
    username = serializers.CharField()
    password = serializers.CharField()


class TokenVerifySerializer(serializers.Serializer):
    """
    Serializer for verifying a provided token. It contains:
    - `token`: The token to be verified.

    The `validate_token` method is used to check if the provided token is valid.
    If the token is not valid, a `ValidationError` is raised.
    """
    token = serializers.CharField()

    def validate_token(self, token):
        if not verify_token(request=self.context["request"], raw_token=token):
            raise serializers.ValidationError("Invalid token")
        return token


class RefreshTokenSerializer(serializers.Serializer):
    """
    Serializer for handling token refresh requests. It contains:
    - `refresh_token`: The refresh token used to obtain a new access token.
    """
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model. It defines which fields of the User model
    should be included in the serialized representation:
    - `id`: The unique identifier of the user.
    - `username`: The username of the user.
    - `email`: The email address of the user.
    """
    class Meta:
        model = User
        fields = ("id", "username", "email")
