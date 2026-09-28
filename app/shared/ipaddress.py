from ipaddress import IPv4Address, IPv6Address, ip_address

from fastapi import Request

type IPAddress = IPv4Address | IPv6Address


def get_client_ip(request: Request) -> IPAddress | None:
    if request.client is None:
        return None

    return ip_address(request.client.host)
