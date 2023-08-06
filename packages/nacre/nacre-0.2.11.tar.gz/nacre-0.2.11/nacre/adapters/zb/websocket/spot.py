import asyncio
import hashlib
import hmac
import json
import time
from typing import Any, Awaitable, Callable, Dict, List, Optional  # noqa: TYP001

from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import Logger

from nacre.adapters.zb.common import format_market
from nacre.adapters.zb.common import format_websocket_market
from nacre.adapters.zb.websocket.client import ZbWebSocketClient


class ZbSpotWebSocket(ZbWebSocketClient):
    """
    Provides access to the `Zb SPOT` streaming WebSocket API.
    """

    BASE_URL = "wss://api.zb.cafe/websocket"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        base_url: Optional[str] = None,
    ):
        super().__init__(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=base_url or self.BASE_URL,
        )

    async def on_post_connect(self):
        if self._subscriptions:
            await self._resubscribe()

    async def ping(self):
        if not self.retrying:
            await self.send("ping".encode())

    async def _subscribe_channel(self, channel: str, **kwargs):
        kwargs["event"] = "addChannel"

        await super()._subscribe_channel(channel, **kwargs)

    async def subscribe_markets(self):
        await self._subscribe_channel(channel="markets")

    async def subscribe_ticker(self, symbol: str):
        channel = f"{format_websocket_market(symbol)}_ticker"
        await self._subscribe_channel(channel=channel)

    async def subscribe_depth(self, symbol: str):
        channel = f"{format_websocket_market(symbol)}_depth"
        await self._subscribe_channel(channel=channel)

    async def subscribe_trades(self, symbol: str):
        channel = f"{format_websocket_market(symbol)}_trades"
        await self._subscribe_channel(channel=channel)


class ZbSpotUserDataWebSocket(ZbWebSocketClient):
    BASE_URL = "wss://api.zb.cafe/websocket"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        key: str,
        hashed_secret: str,
        socks_proxy: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        super().__init__(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=base_url or self.BASE_URL,
            socks_proxy=socks_proxy,
        )

        self._key = key
        self._hashed_secret = hashed_secret
        self.is_logged_in = False
        self._post_connect_callbacks: List[Callable[..., Awaitable]] = []

    async def ping(self):
        if not self.retrying:
            await self.send("ping".encode())

    def add_after_connect_callback(self, callback: Callable[..., Awaitable]):
        self._post_connect_callbacks.append(callback)

    async def on_post_connect(self):
        await self.subscribe_asset_snapshot()
        for callback in self._post_connect_callbacks:
            await callback()

        self.is_logged_in = True

    async def _subscribe_channel(self, channel: str, **kwargs):
        kwargs["event"] = "addChannel"
        kwargs["accesskey"] = self._key
        kwargs["sign"] = self._get_sign(channel, kwargs)
        await super()._subscribe_channel(channel, **kwargs)

    async def logged_in(self):
        while not self.is_logged_in:
            await self._sleep0()
        self._log.debug("Websocket logged in")

    def _get_sign(self, channel: str, payload: Dict[str, Any]) -> str:
        params = {"channel": channel, **payload}
        sorted_params = dict(sorted(params.items()))
        query_string = json.dumps(sorted_params, separators=(",", ":"))
        return hmac.new(
            bytes(self._hashed_secret, encoding="utf-8"), query_string.encode("utf-8"), hashlib.md5
        ).hexdigest()

    async def subscribe_recent_order(self, market: str) -> None:
        payload = {
            "market": f"{format_market(market)}",
        }
        await self._subscribe_channel(channel="push_user_record", **payload)

    async def subscribe_order_update(self, market: str) -> None:
        payload = {
            "market": f"{format_market(market)}",
        }
        await self._subscribe_channel(channel="push_user_incr_record", **payload)

    async def subscribe_asset_snapshot(self):
        await self._subscribe_channel(channel="push_user_asset")

    async def subscribe_asset_update(self):
        await self._subscribe_channel(channel="push_user_incr_asset")

    async def get_account_info(self):
        payload = {"no": str(int(time.time() * 1000))}
        await self._subscribe_channel(channel="getaccountinfo", **payload)
