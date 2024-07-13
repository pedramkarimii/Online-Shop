from typing import Dict
from django.http import HttpRequest
from rest_framework_simplejwt.tokens import Token, UntypedToken
from rest_framework_simplejwt.tokens import TokenError as BaseTokenError
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .app_settings import app_setting
from apps.account.users_auth.encryption import encrypt, decrypt
from apps.account.users_auth.exceptions import TokenError
from apps.account.users_auth.client import get_client_info
from apps.account.models import UserAuth
from datetime import datetime
from django.db.models.fields.files import File
from apps.account.users_auth.constants import ACCESS_TOKEN, REFRESH_TOKEN, UUID_FIELD, USER_ID, TOKEN_TYPE, DEVICE_NAME, \
    IP_ADDRESS
from apps.account.users_auth.services import get_user_auth_uuid, update_user_auth_uuid, get_user_auth

User = get_user_model()


class AccessToken(Token):
    lifetime = app_setting.access_token_lifetime
    token_type = ACCESS_TOKEN


class RefreshToken(Token):
    lifetime = app_setting.refresh_token_lifetime
    token_type = REFRESH_TOKEN


def set_token_claims(*, token: Token, claims: Dict, **kwargs):
    """
    Set claims (data fields) on a given token based on provided kwargs.
    Args:
    - token (Token): The token object to set claims on.
    - claims (Dict): Dictionary containing claim names and their values.
    - **kwargs: Additional key-value pairs to set as claims on the token.
    """
    for key in claims:
        claims[key] = kwargs[key]

    for key, value in claims.items():
        if isinstance(value, File):
            token[key] = value.url
        elif isinstance(value, File):
            token[key] = value.url
        elif isinstance(value, datetime):
            token[key] = str(value)
        else:
            token[key] = value


def get_token_claims(*, token: Token, claims: Dict):
    """
    Retrieve claims (data fields) from a given token and store them in the claims dictionary.
    Args:
    - token (Token): The token object to retrieve claims from.
    - claims (Dict): Dictionary to store retrieved claim names and their values.
    """
    for key in claims:
        claims[key] = token.get(key)


def generate_refresh_token_with_claims(**kwargs) -> str:
    """
    Generate a refresh token with specified claims.
    Args:
    - **kwargs: Key-value pairs representing token claims (e.g., user ID, UUID, device info).
    Returns:
    - str: Encrypted refresh token string.
    """
    refresh_token = RefreshToken()

    if app_setting.get_device_limit:
        user_auth = get_user_auth(user_id=kwargs[USER_ID], token_type=UserAuth.REFRESH_TOKEN)
        if user_auth.device_login_count >= app_setting.get_device_limit:
            user_auth.device_login_count = 0
            uuid = update_user_auth_uuid(user_id=kwargs[USER_ID], token_type=UserAuth.REFRESH_TOKEN)
            kwargs[UUID_FIELD] = uuid
            user_auth.uuid = uuid
        else:
            kwargs[UUID_FIELD] = str(user_auth.uuid)
        user_auth.device_login_count += 1
        user_auth.save()
    else:
        kwargs[UUID_FIELD] = get_user_auth_uuid(user_id=kwargs[USER_ID], token_type=UserAuth.REFRESH_TOKEN)

    set_token_claims(token=refresh_token, claims=app_setting.refresh_token_claims, **kwargs)

    refresh_token = encrypt_token(refresh_token)

    return refresh_token


def generate_access_token_with_claims(**kwargs) -> str:
    """
    Generate an access token with specified claims.
    Args:
    - **kwargs: Key-value pairs representing token claims (e.g., user ID, UUID, device info).
    Returns:
    - str: Encrypted access token string.
    """
    access_token = AccessToken()

    if app_setting.get_device_limit:
        user_auth = get_user_auth(user_id=kwargs[USER_ID], token_type=UserAuth.ACCESS_TOKEN)
        if user_auth.device_login_count >= app_setting.get_device_limit:
            user_auth.device_login_count = 0
            uuid = update_user_auth_uuid(user_id=kwargs[USER_ID], token_type=UserAuth.ACCESS_TOKEN)
            kwargs[UUID_FIELD] = uuid
            user_auth.uuid = uuid
        else:
            kwargs[UUID_FIELD] = str(user_auth.uuid)
        user_auth.device_login_count += 1
        user_auth.save()
    else:
        kwargs[UUID_FIELD] = get_user_auth_uuid(user_id=kwargs[USER_ID], token_type=UserAuth.ACCESS_TOKEN)

    set_token_claims(token=access_token, claims=app_setting.access_token_claims, **kwargs)

    access_token = encrypt_token(access_token)

    return access_token


def get_user_by_access_token(token: Token) -> User:
    """
    Retrieve a user object based on the claims extracted from an access token.
    Args:
    - token (Token): Access token containing user claims.
    Returns:
    - User: User object based on the token claims.
    """
    claims = app_setting.access_token_user_field_claims

    get_token_claims(token=token, claims=claims)

    return User(
        **claims
    )


def encrypt_token(token: Token) -> str:
    """
    Encrypt a token object to produce an encrypted token string.
    Args:
    - token (Token): Token object to be encrypted.
    Returns:
    - str: Encrypted token string.
    Raises:
    - TokenError: If encryption fails.
    """
    try:
        encrypted_token = encrypt(data=str(token), key=app_setting.encrypt_key)
    except ValueError as err:
        raise TokenError(err)
    return encrypted_token


def decrypt_token(token: str) -> str:
    """
    Decrypt an encrypted token string to retrieve the original token data.
    Args:
    - token (str): Encrypted token string to be decrypted.
    Returns:
    - str: Decrypted token data.
    Raises:
    - TokenError: If decryption fails.
    """
    try:
        decrypted_token = decrypt(encrypted=token.encode(), key=app_setting.encrypt_key)
    except ValueError as err:
        raise TokenError(err)
    return decrypted_token


def generate_token(request: HttpRequest, user: User) -> Dict:
    """
    Generate access and refresh tokens for a given user based on client request information.
    Args:
    - request (HttpRequest): HTTP request object containing client information.
    - user (User): User object for whom tokens are generated.
    Returns:
    - Dict: Dictionary containing access and refresh tokens.
    """
    client_info = get_client_info(request=request)
    refresh_token = generate_refresh_token_with_claims(**client_info, **user.__dict__)

    access_token = generate_access_token_with_claims(**client_info, **user.__dict__)

    user.last_login = now()
    user.save()

    return {
        ACCESS_TOKEN: access_token,
        REFRESH_TOKEN: refresh_token,
    }


def validate_refresh_token(token: Token, client_info: Dict) -> None:
    """
    Validate a refresh token against client information.
    Args:
    - token (Token): Refresh token to be validated.
    - client_info (Dict): Dictionary containing client information (e.g., device name).
    Raises:
    - TokenError: If token validation fails.
    """
    if client_info[DEVICE_NAME] != token[DEVICE_NAME]:
        raise TokenError("invalid token")
    uuid_field = get_user_auth_uuid(user_id=token[USER_ID], token_type=UserAuth.REFRESH_TOKEN)
    if uuid_field != token[UUID_FIELD]:
        raise TokenError("invalid uuid")


def validate_access_token(token: Token, client_info: Dict) -> None:
    """
    Validate an access token against client information.
    Args:
    - token (Token): Access token to be validated.
    - client_info (Dict): Dictionary containing client information (e.g., device name, IP address).
    Raises:
    - TokenError: If token validation fails.
    """
    if client_info[DEVICE_NAME] != token[DEVICE_NAME] or client_info[IP_ADDRESS] != token[IP_ADDRESS]:
        raise TokenError("invalid token")
    uuid_field = get_user_auth_uuid(user_id=token[USER_ID], token_type=UserAuth.ACCESS_TOKEN)
    if uuid_field != token[UUID_FIELD]:
        raise TokenError("invalid token")


def validate_token(request: HttpRequest, raw_token: str) -> Token:
    """
    Validate and decrypt a token string to retrieve the token object.
    Args:
    - request (HttpRequest): HTTP request object containing client information.
    - raw_token (str): Raw token string to be validated and decrypted.
    Returns:
    - Token: Validated and decrypted token object.
    Raises:
    - TokenError: If token validation or decryption fails.
    """
    string_token = decrypt_token(token=raw_token)
    try:
        token = UntypedToken(token=string_token)
    except BaseTokenError as err:
        raise TokenError(err)

    client_info = get_client_info(request=request)

    if token[TOKEN_TYPE] == REFRESH_TOKEN:
        validate_refresh_token(token=token, client_info=client_info)
    elif token[TOKEN_TYPE] == ACCESS_TOKEN:
        validate_access_token(token=token, client_info=client_info)

    return token


def refresh_access_token(request: HttpRequest, raw_refresh_token: str) -> str:
    """
    Refresh an access token based on a provided refresh token.
    Args:
    - request (HttpRequest): HTTP request object containing client information.
    - raw_refresh_token (str): Raw refresh token string to generate a new access token.
    Returns:
    - str: Encrypted new access token string.
    Raises:
    - TokenError: If token validation or generation fails.
    """
    token = validate_token(request=request, raw_token=raw_refresh_token)

    client_info = get_client_info(request=request)

    validate_refresh_token(token=token, client_info=client_info)

    try:
        user = User.objects.get(id=token[USER_ID])
    except User.DoesNotExist as err:
        raise TokenError(err)

    user.last_login = now()
    user.save()

    return generate_access_token_with_claims(**user.__dict__, **client_info)


def verify_token(request: HttpRequest, raw_token: str) -> bool:
    """
    Verify if a token string is valid.
    Args:
    - request (HttpRequest): HTTP request object containing client information.
    - raw_token (str): Raw token string to be verified.
    Returns:
    - bool: True if the token is valid, False otherwise.
    """
    try:
        validate_token(request=request, raw_token=raw_token)
    except TokenError:
        return False
    return True
