from enum import Enum
from typing import List, Optional

import httpx

from pyttrex.api import API_ROOT


class CurrencyStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class Currency:
    symbol: str  # unique symbol for this currency
    name: str  # long name of this currency
    coinType: str  # coin type of this currency
    status: CurrencyStatus  # currency status(online, offline, etc.)
    minConfirmations: int  # minimum number of confirmations
    notice: str  # news or alerts regarding this currency
    txFee: float  # transaction fee for this currency

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


def get_currencies() -> Optional[List[Currency]]:
    r = httpx.get(f"{API_ROOT}/currencies")
    if not r.is_success:
        return None
    json = r.json()
    result = list(map(lambda c: Currency(c), json))
    return result


def get_currency(symbol: str) -> Optional[Currency]:
    if not symbol or not len(symbol):
        return None
    r = httpx.get(f"{API_ROOT}/currencies/{symbol}")
    if not r.is_success:
        return None
    json = r.json()
    result = Currency(json)
    return result
