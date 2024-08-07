import uuid
from django.db import IntegrityError
from apps.account.models import UserAuth
from apps.account.users_auth.cache import get_cache, set_cache
from apps.account.users_auth.app_settings import app_setting

ACCESS_UUID_CACHE_KEY = "user:{user_id}:access:uuid"
REFRESH_UUID_CACHE_KEY = "user:{user_id}:refresh:uuid"

TOKEN_TYPE_KEY = {
    UserAuth.ACCESS_TOKEN: ACCESS_UUID_CACHE_KEY,
    UserAuth.REFRESH_TOKEN: REFRESH_UUID_CACHE_KEY,
}


def save_user_auth_uuid(user_auth) -> UserAuth:
    """
    Generate and save a new UUID for user authentication.
    Args:
    - user_auth (UserAuth): UserAuth object to which the UUID will be assigned.
    Returns:
    - UserAuth: The updated UserAuth object with the generated UUID.
    """
    while True:
        try:
            user_auth.uuid = uuid.uuid4()
            user_auth.save()
            return user_auth
        except IntegrityError:
            pass


def create_user_auth(user_id: int, token_type: int, uuid_filed: uuid.UUID | None = None) -> UserAuth:
    """
    Create a new UserAuth entry for user authentication.
    Args:
    - user_id (int): The ID of the user.
    - token_type (int): The type of token (access or refresh).
    - uuid_field (Optional[uuid.UUID]): Optional UUID to assign to the UserAuth entry.
    Returns:
    - UserAuth: The created or updated UserAuth object.
    """
    user_auth = UserAuth(user_id=user_id, token_type=token_type)
    if uuid_filed:
        user_auth.uuid = uuid_filed
        user_auth.save()
    else:
        user_auth = save_user_auth_uuid(user_auth=user_auth)
    return user_auth


def get_user_auth_uuid(user_id: int, token_type: int) -> str:
    """
    Retrieve the UUID associated with a user and token type.
    Args:
    - user_id (int): The ID of the user.
    - token_type (int): The type of token (access or refresh).
    Returns:
    - str: The UUID as a string.
    """
    if app_setting.cache_using:
        access_uuid = get_cache(key=TOKEN_TYPE_KEY[token_type].format(user_id=user_id))
        if access_uuid:
            return access_uuid

    user_auths = UserAuth.objects.filter(user_id=user_id, token_type=token_type)
    if user_auths.exists():
        user_auth = user_auths.first()
    else:
        user_auth = create_user_auth(user_id=user_id, token_type=token_type)

    if app_setting.cache_using:
        set_cache(key=TOKEN_TYPE_KEY[token_type].format(user_id=user_id), value=str(user_auth.uuid),
                  timeout=60 * 60 * 24 * 30)

    return str(user_auth.uuid)


def get_user_auth(user_id: int, token_type: int) -> UserAuth:
    """
    Retrieve the UserAuth object associated with a user and token type.
    Args:
    - user_id (int): The ID of the user.
    - token_type (int): The type of token (access or refresh).
    Returns:
    - UserAuth: The UserAuth object.
    """
    user_auths = UserAuth.objects.filter(user_id=user_id, token_type=token_type)
    if user_auths.exists():
        user_auth = user_auths.first()
        if app_setting.cache_using and not get_cache(key=TOKEN_TYPE_KEY[token_type].format(user_id=user_id)):
            set_cache(key=TOKEN_TYPE_KEY[token_type].format(user_id=user_id), value=str(user_auth.uuid),
                      timeout=60 * 60 * 24 * 30)
    else:
        user_auth = create_user_auth(user_id=user_id, token_type=token_type)
        if app_setting.cache_using:
            set_cache(key=TOKEN_TYPE_KEY[token_type].format(user_id=user_id), value=str(user_auth.uuid),
                      timeout=60 * 60 * 24 * 30)

    return user_auth


def update_user_auth_uuid(user_id: int, token_type: int) -> str:
    """
    Update the UUID associated with a user and token type.
    Args:
    - user_id (int): The ID of the user.
    - token_type (int): The type of token (access or refresh).
    Returns:
    - str: The updated UUID as a string.
    """
    user_auths = UserAuth.objects.filter(user_id=user_id, token_type=token_type)
    if user_auths.exists():
        user_auth = user_auths.first()
        user_auth = save_user_auth_uuid(user_auth=user_auth)
    else:
        user_auth = create_user_auth(user_id=user_id, token_type=token_type)

    if app_setting.cache_using:
        set_cache(key=TOKEN_TYPE_KEY[token_type].format(user_id=user_id), value=str(user_auth.uuid),
                  timeout=60 * 60 * 24 * 30)

    return str(user_auth.uuid)
