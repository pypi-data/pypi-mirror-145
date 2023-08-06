from enum import Enum
from typing import Optional, List

import httpx

from pyttrex.api import API_ROOT


class MarketStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class Market:
    symbol: str
    baseCurrencySymbol: str
    quoteCurrencySymbol: str
    minTradeSize: int
    precision: int
    status: MarketStatus
    createdAt: str
    notice: str

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


def get_markets() -> Optional[List[Market]]:
    r = httpx.get(f"{API_ROOT}/markets")
    if not r.is_success:
        return None
    json = r.json()
    result = list(map(lambda m: Market(m), json))
    return result


def get_market(symbol: str) -> Optional[Market]:
    if not symbol or not len(symbol):
        return None
    r = httpx.get(f"{API_ROOT}/markets/{symbol}")
    if not r.is_success:
        return None
    json = r.json()
    result = Market(json)
    return result


class MarketSummary:
    symbol: str
    high: float
    low: float
    volume: float
    quoteVolume: float
    percentChange: float
    updatedAt: str

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


def get_market_summaries() -> Optional[List[MarketSummary]]:
    r = httpx.get(f"{API_ROOT}/markets/summaries")
    if not r.is_success:
        return None
    json = r.json()
    result = list(map(lambda m: MarketSummary(m), json))
    return result


def get_market_summary(symbol: str) -> Optional[MarketSummary]:
    if not symbol or not len(symbol):
        return None
    r = httpx.get(f"{API_ROOT}/markets/{symbol}/summary")
    if not r.is_success:
        return None
    json = r.json()
    result = MarketSummary(json)
    return result


class Ticker:
    symbol: str
    lastTradeRate: float
    bidRate: float
    askRate: float

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


def get_tickers() -> Optional[List[Ticker]]:
    r = httpx.get(f"{API_ROOT}/markets/tickers")
    if not r.is_success:
        return None
    json = r.json()
    result = list(map(lambda m: Ticker(m), json))
    return result


def get_ticker(symbol: str) -> Optional[Ticker]:
    if not symbol or not len(symbol):
        return None
    r = httpx.get(f"{API_ROOT}/markets/{symbol}/ticker")
    if not r.is_success:
        return None
    json = r.json()
    result = Ticker(json)
    return result


class OrderBookEntry:
    quantity: float
    rate: float

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


class OrderBook:
    bid: List[OrderBookEntry]
    ask: List[OrderBookEntry]

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            if k == 'bid':
                self.bid = list(map(lambda t: OrderBookEntry(t), v))
            elif k == 'ask':
                self.ask = list(map(lambda t: OrderBookEntry(t), v))
            else:
                setattr(self, k, v)


def get_order_book(symbol: str) -> Optional[OrderBook]:
    if not symbol or not len(symbol):
        return None
    r = httpx.get(f"{API_ROOT}/markets/{symbol}/orderbook")
    if not r.is_success:
        return None
    json = r.json()
    result = OrderBook(json)
    return result


class Trade:
    id: str
    executedAt: str
    quantity: float
    rate: float
    takerSide: str

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


def get_trades(symbol: str) -> Optional[List[Trade]]:
    if not symbol or not len(symbol):
        return None
    r = httpx.get(f"{API_ROOT}/markets/{symbol}/trades")
    if not r.is_success:
        return None
    json = r.json()
    result = list(map(lambda t: Trade(t), json))
    return result
