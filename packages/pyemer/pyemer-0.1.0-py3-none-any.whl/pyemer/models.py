from enum import Enum
from dataclasses import dataclass
from typing import Union


@dataclass
class NVSRecord:
    name: str
    value: Union[str, bytes]
    type: str = None

    def __post_init__(self):
        l = self.name.split(":")
        t = None
        try:
            l[1]
            self.type = l[0]
        except IndexError:
            pass

    def __repr__(self) -> str:
        return self.name + "=" + self.value


@dataclass
class EmcAddress:
    address: str
    balance: float = None

    def __repr__(self) -> str:
        return self.address


@dataclass
class Transaction:
    tx_id: str
    timestamp: int
    height: int = None

    def __repr__(self) -> str:
        return self.tx_id


@dataclass
class NVSTx:
    record: NVSRecord
    address: EmcAddress
    tx: Transaction
    days: int = None


class ValueType(Enum):
    hex = "hex"
    base64 = "base64"
