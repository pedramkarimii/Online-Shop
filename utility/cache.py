from typing import Any

from django.core.cache import cache


def get_or_create(key: str, value: Any, timeout: int = 1):
    """Get value from cache by key or create it if not exists.

        Args:
            key (str): The key to lookup in cache.
            value (Any): The value to be cached if key does not exist.
            timeout (int, optional): Timeout for cache expiration in seconds. Defaults to 1.

        Returns:
            Any: The value from cache if found, otherwise the newly created value.
        """
    if not (data := cache.get(key, None)):
        if callable(value):
            value = value()

        cache.set(key, value, timeout)
    return data
