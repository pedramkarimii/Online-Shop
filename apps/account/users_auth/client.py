import ipaddress
from typing import Dict

from django.http import HttpRequest

from .constants import IP_ADDRESS, DEVICE_NAME


def get_ip_address(request: HttpRequest) -> str:
    """
    Retrieve the client's IP address from the HTTP request.
    Args:
    - request (HttpRequest): The HTTP request object.
    Returns:

    """
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip_address:
        ip_address = ip_address.split(",")[0]
    else:
        ip_address = request.META.get("REMOTE_ADDR", '').split(",")[0]

    possibles = (ip_address.lstrip("[").split("]")[0], ip_address.split(":")[0])

    for addr in possibles:
        try:
            return str(ipaddress.ip_address(addr))
        except:
            pass

    return ip_address


def get_client_info(request: HttpRequest) -> Dict:
    """
    Retrieve client information including device name and IP address from the HTTP request.
    Args:
    - request (HttpRequest): The HTTP request object.
    Returns:
    - Dict: A dictionary containing client information with keys 'DEVICE_NAME' and 'IP_ADDRESS'.
    """
    return {
        DEVICE_NAME: request.META.get('HTTP_USER_AGENT', ''),
        IP_ADDRESS: get_ip_address(request=request)
    }
