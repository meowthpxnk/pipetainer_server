from fastapi import WebSocket

from app import redis
from app.constants import WSManagerConstants
from app.schemas import (
    WebsocketResponse,
    WebsocketResponseDeviceData,
    WebsocketRootConnection,
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    def cache_data(self, response: WebsocketResponse) -> None:
        key = WSManagerConstants.DEVICE_CACHE_PATTERN + response.device_name

        data = redis.get(key)

        if not data:
            redis.set(key, response.data.model_dump_json())
            return

        data = WebsocketResponseDeviceData.model_validate_json(data)

        data = data.model_dump()

        for k, v in response.data.model_dump(exclude_unset=True).items():
            data[k] = v

        data = WebsocketResponseDeviceData.model_validate(data)

        redis.set(key, data.model_dump_json())

    def get_cache(self) -> list[WebsocketResponse]:
        keys = redis.keys(WSManagerConstants.DEVICE_CACHE_PATTERN + "*")
        dump = []

        for key in keys:
            key = key.decode()
            device_name = key.replace(
                WSManagerConstants.DEVICE_CACHE_PATTERN, ""
            )
            data = WebsocketResponseDeviceData.model_validate_json(
                redis.get(key)
            )

            dump.append(WebsocketResponse(device_name=device_name, data=data))
        return dump

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

        cache = self.get_cache()

        response = WebsocketRootConnection(data=cache)
        await websocket.send_text(response.model_dump_json())

        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_data(self, response: WebsocketResponse) -> None:
        self.cache_data(response)

        for connection in self.active_connections:
            await connection.send_text(
                response.model_dump_json(exclude_unset=True)
            )
