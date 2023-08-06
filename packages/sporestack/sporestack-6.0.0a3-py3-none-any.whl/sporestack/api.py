"""

SporeStack API request/response models

"""


from typing import List, Optional

from pydantic import BaseModel

from .models import NetworkInterface, Payment

LATEST_API_VERSION = 3


class TokenEnable:
    """Deprecated: Use TokenAdd instead."""

    url = "/token/{token}/enable"
    method = "POST"

    class Request(BaseModel):
        currency: str
        dollars: int
        affiliate_token: Optional[str] = None

    class Response(BaseModel):
        token: str
        payment: Payment


class TokenAdd:
    url = "/token/{token}/add"
    method = "POST"

    class Request(BaseModel):
        currency: str
        dollars: int
        affiliate_token: Optional[str] = None

    class Response(BaseModel):
        token: str
        payment: Payment


class TokenBalance:
    url = "/token/{token}/balance"
    method = "GET"

    class Response(BaseModel):
        token: str
        cents: int
        usd: str


class ServerLaunch:
    url = "/server/{machine_id}/launch"
    method = "POST"

    class Request(BaseModel):
        machine_id: str
        days: int
        flavor: str
        ssh_key: str
        operating_system: str
        currency: Optional[str] = None
        """Currency only needs to be set if not paying with a token."""
        region: Optional[str] = None
        organization: Optional[str] = None
        token: Optional[str] = None
        quote: bool = False
        affiliate_token: Optional[str] = None
        affiliate_amount: None = None
        """Deprecated field"""
        settlement_token: Optional[str] = None
        """Deprecated field. Use token instead."""

    class Response(BaseModel):
        payment: Payment
        expiration: int
        machine_id: str
        operating_system: str
        flavor: str
        network_interfaces: List[NetworkInterface] = []
        created_at: int = 0
        region: Optional[str] = None
        latest_api_version: int = LATEST_API_VERSION
        created: bool = False
        paid: bool = False
        warning: Optional[str] = None
        txid: Optional[str] = None


class ServerTopup:
    url = "/server/{machine_id}/topup"
    method = "POST"

    class Request(BaseModel):
        machine_id: str
        days: int
        token: Optional[str] = None
        quote: bool = False
        currency: Optional[str] = None
        """Currency only needs to be set if not paying with a token."""
        affiliate_token: Optional[str] = None
        affiliate_amount: None = None
        """Deprecated field"""
        settlement_token: Optional[str] = None
        """Deprecated field. Use token instead."""

    class Response(BaseModel):
        machine_id: str
        payment: Payment
        expiration: int
        paid: bool = False
        warning: Optional[str] = None
        txid: Optional[str] = None
        latest_api_version: int = LATEST_API_VERSION


class ServerInfo:
    url = "/server/{machine_id}/info"
    method = "GET"

    class Response(BaseModel):
        created_at: int
        expiration: int
        running: bool
        machine_id: str
        network_interfaces: List[NetworkInterface]
        region: str


class ServerStart:
    url = "/server/{machine_id}/start"
    method = "POST"


class ServerStop:
    url = "/server/{machine_id}/stop"
    method = "POST"


class ServerDelete:
    url = "/server/{machine_id}/delete"
    method = "POST"


class ServerRebuild:
    url = "/server/{machine_id}/rebuild"
    method = "POST"
