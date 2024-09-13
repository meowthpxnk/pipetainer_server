from fastapi import APIRouter

from app import docker_client
from app.database.models import User
from app.schemas import ImageSchema, PullImageForm
from app.schemas import User as UserSchema

from ._dependencies import AdminRules


images_routes = APIRouter(prefix="/image")


@images_routes.post("/pull", dependencies=[AdminRules])
def load_image(form: PullImageForm):
    docker_client.pull_image(form.image_name)


@images_routes.get("")
async def get_images():
    images = await docker_client.get_images()
    print(images)

    dump_images = []

    for image in images.images:
        if image.tags:
            for tag in image.tags:
                dump_images.append(
                    ImageSchema(image_name=f"{image.name}:{tag}")
                )
    return dump_images


@images_routes.delete("/{image_name}", dependencies=[AdminRules])
async def delete_image(image_name: str):
    print(image_name)
    return await docker_client.delete_image(image_name)


@images_routes.patch("/{image_name}", dependencies=[AdminRules])
def repull_image(image_name: str):
    docker_client.repull_image(image_name)


@images_routes.patch(
    "/{repo_owner}/{repository}",
    dependencies=[AdminRules],
    include_in_schema=False,
)
def repull_image_repo(repo_owner: str, repository: str):
    repull_image(f"{repo_owner}/{repository}")


@images_routes.delete(
    "/{repo_owner}/{repository}",
    dependencies=[AdminRules],
    include_in_schema=False,
)
async def delete_image_repo(repo_owner: str, repository: str):
    return await delete_image(f"{repo_owner}/{repository}")
