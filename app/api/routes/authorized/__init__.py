from fastapi import APIRouter
from ._dependencies import UserTokenDataDepends
from .session import session_routes
from .user import user_routes
from .api_keys import api_keys_routes
from .servers import servers_routes
from .images import images_routes
from .docker import docker_routes
from .device import device_routes

auth_protect_router = APIRouter(dependencies=[UserTokenDataDepends])

auth_protect_router.include_router(session_routes)
auth_protect_router.include_router(user_routes)
auth_protect_router.include_router(api_keys_routes)
auth_protect_router.include_router(servers_routes)
auth_protect_router.include_router(images_routes)
auth_protect_router.include_router(docker_routes)
auth_protect_router.include_router(device_routes)
