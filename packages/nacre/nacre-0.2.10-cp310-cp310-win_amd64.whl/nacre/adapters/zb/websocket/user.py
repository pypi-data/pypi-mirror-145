import asyncio
import base64
import hashlib
import hmac
import json
import time
from typing import Any, Awaitable, Callable, Dict, List, Optional  # noqa: TYP001
from urllib.parse import urlparse

import orjson
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import Logger

from nacre.adapters.zb.common import format_market
from nacre.adapters.zb.common import format_symbol
from nacre.adapters.zb.websocket.client import ZbWebSocketClient


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


class ZbFutureUserDataWebSocket:
    BASE_URL = "wss://fapi.zb.com/ws/private/api/v2"

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
        usdt_m = ZbFutureWebSocket(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=base_url or self.BASE_URL,
            key=key,
            hashed_secret=hashed_secret,
            futures_account_type=1,
            socks_proxy=socks_proxy,
        )

        # force path replace
        qc_ws_url = (
            urlparse(base_url or self.BASE_URL)._replace(path="/qc/ws/private/api/v2").geturl()
        )

        qc_m = ZbFutureWebSocket(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=qc_ws_url,
            key=key,
            hashed_secret=hashed_secret,
            futures_account_type=2,
            socks_proxy=socks_proxy,
        )

        self.clients = {"usdt": usdt_m, "qc": qc_m}

    @property
    def is_connected(self) -> bool:
        return all(map(lambda c: c.is_connected, self.clients.values()))

    async def connect(self):
        for client in self.clients.values():
            await client.connect()

    async def disconnect(self):
        # very weird bug here, can't await both otherwise it will stuck at return
        await self.clients["usdt"].disconnect()
        # await self.clients["qc"].disconnect()
        # for client in self.clients.values():
        #     await client.disconnect()

    async def logged_in(self):
        for client in self.clients.values():
            await client.logged_in()

    def get_client(self, symbol: str):
        quote = symbol.partition("/")[2]
        if quote == "ZUSD":
            quote = "usdt"
        return self.clients[quote.lower()]

    async def subscribe_funding_update(self, currency: str):
        for client in self.clients.values():
            await client.subscribe_funding_update(currency)

    async def subscribe_asset_update(self):
        for client in self.clients.values():
            await client.subscribe_asset_update()

    async def get_asset_snapshot(self, currency: str):
        for client in self.clients.values():
            await client.get_asset_snapshot(currency)

    async def subscribe_position_update(self, symbol: Optional[str] = None):
        if symbol is not None:
            client = self.get_client(symbol)
            await client.subscribe_position_update(symbol)
        else:
            for client in self.clients.values():
                await client.subscribe_position_update()

    async def subscribe_order_update(self, symbol: Optional[str] = None):
        if symbol is not None:
            client = self.get_client(symbol)
            await client.subscribe_order_update(symbol)
        else:
            for client in self.clients.values():
                await client.subscribe_order_update()

    async def new_order(
        self,
        symbol: str,
        side: int,
        amount: float,
        price: Optional[float] = None,
        action: Optional[int] = None,
        client_order_id: Optional[str] = None,
    ):
        client = self.get_client(symbol)
        await client.new_order(symbol, side, amount, price, action, client_order_id)

    async def cancel_order(
        self,
        symbol: str,
        order_id: Optional[str] = None,
        client_order_id: Optional[str] = None,
    ):
        client = self.get_client(symbol)
        await client.cancel_order(symbol, order_id, client_order_id)

    async def cancel_open_orders(self, symbol: str):
        client = self.get_client(symbol)
        await client.cancel_open_orders(symbol)

    async def get_trade_list(self, symbol: str, order_id: str):
        client = self.get_client(symbol)
        await client.get_trade_list(symbol, order_id)


class ZbFutureWebSocket(ZbWebSocketClient):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        base_url: str,
        key: str,
        hashed_secret: str,
        futures_account_type: int,
        socks_proxy: Optional[str] = None,
    ):
        super().__init__(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=base_url,
            socks_proxy=socks_proxy,
        )

        self._key = key
        self._hashed_secret = hashed_secret
        self.is_logged_in = False
        self.futures_account_type = futures_account_type

    async def _subscribe_channel(self, channel: str, **kwargs):
        kwargs["action"] = "subscribe"

        await super()._subscribe_channel(channel, **kwargs)

    def _get_sign(self, timestamp, http_method, url_path) -> str:
        whole_data = timestamp + http_method + url_path
        m = hmac.new(self._hashed_secret.encode(), whole_data.encode(), hashlib.sha256)
        return str(base64.b64encode(m.digest()), "utf-8")

    async def _login(self):
        """
        Login to the user data stream.

        """
        timestamp = self._clock.utc_now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        signature = self._get_sign(timestamp, "GET", "login")
        payload = {
            "action": "login",
            "ZB-APIKEY": self._key,
            "ZB-TIMESTAMP": timestamp,
            "ZB-SIGN": signature,
        }

        await self.send(orjson.dumps(payload))

    async def logged_in(self):
        while not self.is_logged_in:
            await self._sleep0()
        self._log.debug("Websocket logged in")

    async def on_post_connect(self):
        await self._login()

        await self.subscribe_asset_update()
        await self.subscribe_position_update()
        await self.subscribe_order_update()

        self.is_logged_in = True

    async def subscribe_funding_update(self, currency: str):
        await self._subscribe_channel(
            channel="Fund.change", futuresAccountType=self.futures_account_type, currency=currency
        )

    async def subscribe_asset_update(self):
        await self._subscribe_channel(
            channel="Fund.assetChange", futuresAccountType=self.futures_account_type
        )

    async def get_asset_snapshot(self, currency: str):
        await self._subscribe_channel(
            channel="Fund.balance", futuresAccountType=self.futures_account_type, currency=currency
        )

    async def subscribe_position_update(self, symbol: Optional[str] = None):
        payload: Dict[str, Any] = {"futuresAccountType": self.futures_account_type}
        if symbol:
            payload["symbol"] = format_symbol(symbol)

        await self._subscribe_channel(channel="Positions.change", **payload)

    async def subscribe_order_update(self, symbol: Optional[str] = None):
        payload = {}
        if symbol:
            payload["symbol"] = format_symbol(symbol)

        await self._subscribe_channel(channel="Trade.orderChange", **payload)

    async def new_order(
        self,
        symbol: str,
        side: int,
        amount: float,
        price: Optional[float] = None,
        action: Optional[int] = None,
        client_order_id: Optional[str] = None,
    ):
        payload: Dict[str, Any] = {"symbol": format_symbol(symbol), "side": side, "amount": amount}
        if price is not None:
            payload["price"] = price
        if action is not None:
            payload["actionType"] = action
        if client_order_id is not None:
            payload["clientOrderId"] = client_order_id

        await self._subscribe_channel(channel="Trade.order", **payload)

    async def cancel_order(
        self,
        symbol: str,
        order_id: Optional[str] = None,
        client_order_id: Optional[str] = None,
    ):
        payload: Dict[str, Any] = {"symbol": format_symbol(symbol)}
        if order_id is not None:
            payload["orderId"] = order_id
        elif client_order_id is not None:
            payload["clientOrderId"] = client_order_id

        await self._subscribe_channel(channel="Trade.cancelOrder", **payload)

    async def cancel_open_orders(self, symbol: str):
        payload: Dict[str, Any] = {"symbol": format_symbol(symbol)}
        await self._subscribe_channel(channel="Trade.cancelAllOrders", **payload)

    async def get_trade_list(self, symbol: str, order_id: str):
        payload = {}
        payload["symbol"] = format_symbol(symbol)
        payload["orderId"] = order_id
        await self._subscribe_channel(channel="Trade.getTradeList", **payload)
