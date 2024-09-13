from fastapi import APIRouter

from app import docker_client
from app.database.models import Server
from app.schemas import CreateServerForm
from app.schemas import Server as ServerSchema

from ._dependencies import AdminRules, SupervisorRules


servers_routes = APIRouter(prefix="/server")


@servers_routes.post("/create", dependencies=[SupervisorRules])
async def create_server(form: CreateServerForm):
    Server.exists(form.short_name)
    Server(form).create()


@servers_routes.get("")
async def get_servers():
    return [
        ServerSchema(short_name=server.short_name, url=server.url)
        for server in Server.select_where(all=True)
    ]


@servers_routes.delete("/{short_name}", dependencies=[SupervisorRules])
async def delete_server(short_name: str):
    devices = docker_client.get_devices()
    print(devices)

    devices = docker_client.get_devices()
    response = []

    server = Server.select_where(Server.short_name == short_name)
    for device in devices.devices:
        if device.server_url == server.url:
            raise Exception("The server is in use by devices.")
        response.append(device)
    server.delete()
