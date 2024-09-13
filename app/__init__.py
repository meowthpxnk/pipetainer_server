from .settings import Settings

settings = Settings()

from MeowthLogger import Logger

logger = Logger(logger_level=settings.logger.level.value, use_uvicorn=True)

from redis import Redis

redis = Redis(settings.redis.host, settings.redis.port)
redis.ping()

from .docker_client import DockerClient

docker_client = DockerClient.from_env()

from .auth import AuthService

auth_service = AuthService()

from asyncio import new_event_loop

loop = new_event_loop()


from .api import server, api
from .api.ws_manager.manager import ConnectionManager

device_manager = ConnectionManager()

from .api import routes
