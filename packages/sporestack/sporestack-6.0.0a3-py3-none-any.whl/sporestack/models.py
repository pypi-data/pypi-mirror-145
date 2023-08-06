"""

SporeStack API supplemental models

"""


from typing import Optional

from pydantic import BaseModel


class NetworkInterface(BaseModel):
    ipv4: str
    ipv6: str


class Payment(BaseModel):
    txid: Optional[str]
    uri: Optional[str]
    usd: str
    paid: bool
