from fastapi import APIRouter, Depends

from app import docker_client, settings
from app.database.models import Server
from app.schemas import CreateDeviceForm, Device
from app.schemas import User as UserSchema

from ._dependencies import (
    SupervisorRules,
    TokenData,
    UserTokenDataDepends,
    validate_rules,
)


device_routes = APIRouter(prefix="/device")


@device_routes.post("/create")
async def create_device(form: CreateDeviceForm):
    server = Server.select_where(Server.short_name == form.server_short_name)
    await docker_client.image_exists(form.image)
    await docker_client.create_device(form, server.url)


@device_routes.get("")
def get_devices():
    devices = docker_client.get_devices()
    response = []

    for device in devices.devices:
        server = Server.select_where(Server.url == device.server_url)
        device = Device(
            server_short_name=server.short_name,
            name=device.name,
            image=device.image,
        )
        response.append(device)

    return response


@device_routes.delete("/{device_name}")
def delete_device(device_name: str):
    return docker_client.delete_device(device_name)
