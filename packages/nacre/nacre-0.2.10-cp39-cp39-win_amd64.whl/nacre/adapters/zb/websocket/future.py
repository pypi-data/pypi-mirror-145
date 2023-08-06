import asyncio
from typing import Callable, Optional
from urllib.parse import urlparse

from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import Logger

from nacre.adapters.zb.common import format_symbol
from nacre.adapters.zb.websocket.client import ZbWebSocketClient


class ZbFuturesWebSocket:
    BASE_URL = "wss://fapi.zb.com/ws/public/v1"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        base_url: Optional[str] = None,
    ):

        usdt_m = ZbFuturesWebsocketClient(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=base_url or self.BASE_URL,
        )

        # force path replace
        qc_ws_url = urlparse(base_url or self.BASE_URL)._replace(path="/qc/ws/public/v1").geturl()
        qc_m = ZbFuturesWebsocketClient(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=qc_ws_url,
        )

        self.clients = {"usdt": usdt_m, "qc": qc_m}

    @property
    def is_connected(self) -> bool:
        return all(map(lambda c: c.is_connected, self.clients.values()))

    def get_client(self, symbol: str):
        quote = symbol.partition("/")[2]
        if quote == "ZUSD":
            quote = "usdt"
        return self.clients[quote.lower()]

    async def connect(self):
        aws = []
        for client in self.clients.values():
            aws.append(client.connect())
        await asyncio.gather(*aws)

    async def disconnect(self):
        # very weird bug here, can't await both otherwise it will stuck at return
        await self.clients["usdt"].disconnect()
        # await self.clients["qc"].disconnect()

    async def subscribe_mark_price(self, symbol: str = None):
        for client in self.clients.values():
            await client.subscribe_mark_price(symbol)

    async def subscribe_index_price(self, symbol: str = None):
        for client in self.clients.values():
            await client.subscribe_index_price(symbol)

    async def subscribe_mark_bars(self, symbol: str, interval: str, size: int = 1):
        for client in self.clients.values():
            await client.subscribe_mark_bars(symbol, interval, size)

    async def subscribe_index_bars(self, symbol: str, interval: str, size: int = 1):
        for client in self.clients.values():
            await client.subscribe_index_bars(symbol, interval, size)

    async def subscribe_trades(self, symbol: str, size: int = 50):
        client = self.get_client(symbol)
        await client.subscribe_trades(symbol, size)

    async def subscribe_bars(self, symbol: str, interval: str, size: int = 1):
        client = self.get_client(symbol)
        await client.subscribe_bars(symbol, interval, size)

    async def subscribe_ticker(self, symbol: str = None):
        for client in self.clients.values():
            await client.subscribe_ticker(symbol)

    async def subscribe_book_deltas(
        self, symbol: str, depth: int = 50, precision: Optional[float] = None
    ):
        client = self.get_client(symbol)
        await client.subscribe_book_deltas(symbol, depth, precision)

    async def subscribe_book_snapshot(
        self, symbol: str, depth: int = 5, precision: Optional[float] = None
    ):
        client = self.get_client(symbol)
        await client.subscribe_book_snapshot(symbol, depth, precision)


class ZbFuturesWebsocketClient(ZbWebSocketClient):
    """
    Provides access to the `Zb FUTURES` streaming WebSocket API.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        base_url: str,
    ):
        super().__init__(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=base_url,
        )

    async def on_post_connect(self):
        if self._subscriptions:
            await self._resubscribe()

    async def _subscribe_channel(self, channel: str, **kwargs):
        kwargs["action"] = "subscribe"

        await super()._subscribe_channel(channel, **kwargs)

    async def _unsubscribe_channel(self, channel: str, **kwargs):
        kwargs["action"] = "unsubscribe"
        await super()._unsubscribe_channel(channel, **kwargs)

    async def subscribe_mark_price(self, symbol: str = None):
        chan = "All"
        if symbol:
            chan = format_symbol(symbol)
        await self._subscribe_channel(channel=f"{chan}.mark")

    async def subscribe_index_price(self, symbol: str = None):
        chan = "All"
        if symbol:
            chan = format_symbol(symbol)
        await self._subscribe_channel(channel=f"{chan}.index")

    async def subscribe_mark_bars(self, symbol: str, interval: str, size: int = 1):
        channel = f"{format_symbol(symbol)}.mark_{interval}"
        await self._subscribe_channel(channel=channel, size=size)

    async def subscribe_index_bars(self, symbol: str, interval: str, size: int = 1):
        channel = f"{format_symbol(symbol)}.index_{interval}"
        await self._subscribe_channel(channel=channel, size=size)

    async def subscribe_trades(self, symbol: str, size: int = 50):
        """
        Trade Streams.

        The Trade Streams push raw trade information; each trade has a unique buyer and seller.
        Update Speed: Real-time

        """
        await self._subscribe_channel(channel=f"{format_symbol(symbol)}.Trade", size=size)

    async def subscribe_bars(self, symbol: str, interval: str, size: int = 1):
        """
        Subscribe to bar (kline/candlestick) stream.

        The Kline/Candlestick Stream push updates to the current klines/candlestick every second.
        interval:
        1M,5M,15M, 30M, 1H, 6H, 1D, 5D
        Update Speed: 2000ms

        """
        channel = f"{format_symbol(symbol)}.KLine_{interval}"
        await self._subscribe_channel(channel=channel, size=size)

    async def subscribe_ticker(self, symbol: str = None):
        """
        Individual symbol or all symbols ticker.

        24hr rolling window ticker statistics for a single symbol.
        These are NOT the statistics of the UTC day, but a 24hr rolling window for the previous 24hrs.
        Stream Name: <symbol>@ticker or
        Stream Name: !ticker@arr
        Update Speed: 1000ms

        """
        if symbol is None:
            await self._subscribe_channel(channel="All.Ticker")
        else:
            await self._subscribe_channel(channel=f"{format_symbol(symbol)}.Ticker")

    async def subscribe_book_deltas(
        self, symbol: str, depth: int = 50, precision: Optional[float] = None
    ):
        """
        Partial Book Depth Streams.

        Top bids and asks, Valid are min - 5000, default 50
        Update Speed: real time

        """
        channel = f"{format_symbol(symbol)}.Depth"
        if precision:
            channel = f"{format_symbol(symbol)}.Depth@{precision}"
        await self._subscribe_channel(channel=channel, size=depth)

    async def subscribe_book_snapshot(
        self, symbol: str, depth: int = 5, precision: Optional[float] = None
    ):
        """
        Diff book depth stream.

        Top bids and asks, Valid are 5 - 10
        Update Speed: 200ms
        Order book price and quantity depth updates used to locally manage an order book.

        """
        channel = f"{format_symbol(symbol)}.DepthWhole"
        if precision:
            channel = f"{format_symbol(symbol)}.DepthWhole@{precision}"
        await self._subscribe_channel(channel=channel, size=depth)
