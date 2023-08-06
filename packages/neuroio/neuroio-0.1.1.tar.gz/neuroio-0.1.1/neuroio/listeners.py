import asyncio
import json
from typing import Awaitable, Callable, Dict, List, Optional, Union

from websockets.exceptions import ConnectionClosed
from websockets.legacy.client import WebSocketClientProtocol, connect

from neuroio import constants
from neuroio.utils import repeat


class EventListener:
    def __init__(
        self,
        api_token: str,
        event_handler_func: Callable[[str], Awaitable[None]],
        timeout: Optional[float] = constants.HTTP_CLIENT_TIMEOUT,
    ) -> None:
        """
        Creates and manages single WebSocket Client object, that is used to
        send & receive messages in Events service.
        """
        self.api_token = api_token
        self.event_handler_func = event_handler_func
        self.timeout = timeout
        self.websocket: Optional[WebSocketClientProtocol] = None

    async def listen(self) -> None:
        async for websocket in connect(
            constants.EVENTS_BASE_URL, open_timeout=self.timeout
        ):
            try:
                self.websocket = websocket
                await self.authorize()
                asyncio.create_task(repeat(5, self.ping))
                async for message in websocket:
                    if not isinstance(message, bytes):
                        await self.event_handler_func(message)
            except ConnectionClosed:
                self.websocket = None
                continue

    async def send_json(self, data: Union[List, Dict]) -> None:
        if self.websocket is not None:
            await self.websocket.send(json.dumps(data))

    async def authorize(self) -> None:
        await self.send_json(
            {"action": "AUTH", "data": {"token": self.api_token}}
        )

    async def ping(self) -> None:
        await self.send_json({"action": "PING"})
