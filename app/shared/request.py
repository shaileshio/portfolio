from ipaddress import IPv4Address, IPv6Address, ip_address

from fastapi import Request

type IPAddress = IPv4Address | IPv6Address


def get_ip_address(request: Request) -> IPAddress | None:
    if request.client is None:
        return None

    return ip_address(request.client.host)


def get_user_agent(request: Request) -> str | None:
    return request.headers.get("user-agent")


def get_device_name(request: Request) -> str | None:
    return request.headers.get("host")
