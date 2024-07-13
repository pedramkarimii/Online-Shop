from typing import Any

from django.core.cache import cache


def get_cache(key: Any) -> Any:
    """
    Retrieve a value from the cache based on the provided key.
    Args:
    - key (Any): The key used to fetch the cached value.
    Returns:
    - Any: The cached value corresponding to the key, or None if not found.
    """
    value = cache.get(key=key)
    cache.close()
    return value


def set_cache(key: Any, value: Any, timeout: int) -> None:
    """
    Set a key-value pair in the cache with a specified timeout.
    Args:
    - key (Any): The key under which to store the value in the cache.
    - value (Any): The value to store in the cache.
    - timeout (int): Timeout period in seconds for the cached value.
    """
    cache.set(key=key, value=value, timeout=timeout)
    cache.close()


def delete_cache(key) -> bool:
    """
    Delete a cached value based on the provided key.
    Args:
    - key (Any): The key of the cached value to delete.
    Returns:
    - bool: True if the value was successfully deleted, False otherwise.
    """
    cache_delete = cache.delete(key=key)
    cache.close()
    return cache_delete


def clear_all_cache() -> None:
    """
    Clear all entries from the cache.
    """
    cache.clear()


def incr_cache(key: Any) -> bool:
    """
    Increment the value of a cached integer by 1.
    Args:
    - key (Any): The key of the cached integer value to increment.
    Returns:
    - bool: True if the increment was successful, False otherwise.
    """
    incr = cache.incr(key=key)
    cache.close()
    return incr
