from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect

from app import device_manager
from app.schemas import (
    DeviceQRRequest,
    DeviceStatus,
    DeviceStatusRequest,
    WebsocketResponse,
)


device_routes = APIRouter(prefix="/device")


@device_routes.put("/{device_name}/qr")
async def delete_device(data: DeviceQRRequest, device_name: str):
    response = WebsocketResponse(
        device_name=device_name, data={"qr": data.data_ref}
    )

    await device_manager.send_data(response)


@device_routes.put("/{device_name}/status")
async def delete_device(device_name: str, data: DeviceStatusRequest):
    response = WebsocketResponse(
        device_name=device_name, data={"status": data.status}
    )

    if data.status != DeviceStatus.LOST_REGISTRATION:
        response.data.qr = None

    await device_manager.send_data(response)


@device_routes.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await device_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        device_manager.disconnect(websocket)
