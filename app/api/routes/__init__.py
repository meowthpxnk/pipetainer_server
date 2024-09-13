from app import api
from .auth import auth_router
from .device import device_routes
from .authorized import auth_protect_router


api.include_router(auth_router)
api.include_router(device_routes)
api.include_router(auth_protect_router)
