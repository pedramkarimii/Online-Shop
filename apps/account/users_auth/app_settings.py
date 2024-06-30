import functools
from datetime import timedelta
from Crypto.Random import get_random_bytes
from apps.account.users_auth.client import IP_ADDRESS, DEVICE_NAME
from apps.account.users_auth.constants import USER_ID, UUID_FIELD


class AppSettings:

    def __init__(self, prefix: str, encryption_key: bytes) -> None:
        """
        Initialize the AppSettings instance with a prefix and an encryption key.
        Args:
        - prefix (str): Prefix used to construct settings names.
        - encryption_key (bytes): Key used for encryption.
        """
        self.prefix = prefix
        self.encryption_key = encryption_key

    def _setting(self, name: str, default: object):
        """
       Retrieve a setting value from Django settings, using a default value if not set.

       Args:
       - name (str): Name of the setting.
       - default (object): Default value if setting is not found.
       Returns:
       - object: Retrieved setting value or default value.
       """
        from django.conf import settings
        return getattr(settings, self.prefix + name, default)

    @property
    def access_token_lifetime(self):
        """
        Property to retrieve the access token lifetime from settings, defaulting to 10 minutes.
        Returns:
        - timedelta: Lifetime duration of access tokens.
        """
        return self._setting("ACCESS_TOKEN_LIFETIME", timedelta(minutes=10))

    @property
    def refresh_token_lifetime(self):
        """
        Property to retrieve the refresh token lifetime from settings, defaulting to 30 days.
        Returns:
        - timedelta: Lifetime duration of refresh tokens.
        """
        return self._setting("REFRESH_TOKEN_LIFETIME", timedelta(days=30))

    @property
    def refresh_token_claims(self):
        """
        Property to retrieve the claims for refresh tokens from settings, with default values.
        Returns:
        - dict: Claims associated with refresh tokens, including standard and custom claims.
        """
        return {
            **self._setting("REFRESH_TOKEN_CLAIMS", {"id": 0}),
            USER_ID: 0,
            UUID_FIELD: "",
            IP_ADDRESS: "",
            DEVICE_NAME: "",
        }

    @property
    def access_token_claims(self):
        """
        Property to retrieve the claims for access tokens from settings, with default values.
        Returns:
        - dict: Claims associated with access tokens, including standard and custom claims.
        """
        return {
            **self._setting("ACCESS_TOKEN_CLAIMS", {"id": 0}),
            USER_ID: 0,
            UUID_FIELD: "",
            IP_ADDRESS: "",
            DEVICE_NAME: "",
        }

    @property
    def access_token_user_field_claims(self):
        """
        Property to retrieve specific user field claims for access tokens from settings, with default values.
        Returns:
        - dict: User field claims associated with access tokens.
        """
        return {
            **self._setting("ACCESS_TOKEN_USER_FIELD_CLAIMS", {"id": 0}),
            USER_ID: 0,
        }

    @property
    def encrypt_key(self):
        """
        Property to retrieve the encryption key from settings, defaulting to the provided encryption key.
        Returns:
        - bytes: Encryption key used for cryptographic operations.
        """
        return self._setting("ENCRYPT_KEY", self.encryption_key)

    @property
    def cache_using(self):
        """
        Property to determine if caching is enabled based on settings.
        Returns:
        - bool: True if caching is enabled, False otherwise.
        """
        return self._setting("CACHE_USING", False)

    @property
    def get_user_by_access_token(self):
        """
        Property to determine if user retrieval by access token is enabled based on settings.
        Returns:
        - bool: True if user retrieval by access token is enabled, False otherwise.
        """
        return self._setting("GET_USER_BY_ACCESS_TOKEN", False)

    @property
    def get_device_limit(self):
        """
        Property to retrieve the device limit setting from settings.
        Returns:
        - int or None: Maximum number of devices allowed per user, or None if not set.
        """
        return self._setting("DEVICE_LIMIT", None)


@functools.lru_cache
def jwt_auth_app_settings() -> AppSettings:
    """
    Function to cache and retrieve an instance of AppSettings for JWT authentication.
    Returns:
    - AppSettings: Instance of AppSettings configured with JWT authentication settings.
    """
    return AppSettings("JWT_AUTH_", get_random_bytes(32))


# Retrieve and store the JWT authentication app settings instance.
app_setting = jwt_auth_app_settings()
