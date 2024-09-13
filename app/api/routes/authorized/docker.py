from fastapi import APIRouter

from app import docker_client
from app.database.models import User
from app.schemas import DockerLoginForm
from app.schemas import User as UserSchema

from ._dependencies import AdminRules


docker_routes = APIRouter(prefix="/docker")


@docker_routes.post("/login", dependencies=[AdminRules])
def login(form: DockerLoginForm):
    docker_client.login(username=form.username, password=form.password)
