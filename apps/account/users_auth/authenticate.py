from apps.account.models import User
from typing import Optional, Tuple
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import AuthUser
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import InvalidToken
from apps.account.users_auth.token import get_user_by_access_token, validate_token
from apps.account.users_auth.exceptions import TokenError
from apps.account.users_auth.app_settings import app_setting
from apps.account.users_auth.constants import USER_ID


class JWTAuthentication(BaseJWTAuthentication):
    """Custom authentication backend for authenticating users via email."""

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        """
        Custom authentication method to authenticate a user using JWT tokens.
        Args:
        - request (Request): The HTTP request object.
        Returns:
        - Optional[Tuple[AuthUser, Token]]: Tuple containing authenticated user and token if authentication succeeds, None otherwise.
        Raises:
        - InvalidToken: If the token is invalid or authentication fails.
        """
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = validate_token(request=request, raw_token=raw_token.decode())
        except TokenError:
            raise InvalidToken(
                {
                    "detail": _("Given token not valid for any token type"),
                }
            )

        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token: Token) -> AuthUser:
        """
        Retrieve the authenticated user based on the validated token.
        Args:
        - validated_token (Token): The validated token object.
        Returns:
        - AuthUser: Authenticated user object.
        """
        if app_setting.get_user_by_access_token:
            return get_user_by_access_token(token=validated_token)
        return User.objects.get(id=validated_token[USER_ID])


class EmailAuthBackend:
    """Custom authentication backend for authenticating users via email."""

    def authenticate(self, request, username=None, password=None):  # noqa
        """
       Authenticate a user based on email and password.
       """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):  # noqa
        """
        Retrieve a user by user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user object if found, None otherwise.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
