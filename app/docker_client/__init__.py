from docker import DockerClient

from docker.utils import parse_repository_tag

from app import logger
import aiohttp
from app.schemas import DockerImagesResponse, CreateDeviceForm, DeviceConfigForm, DockerImage, DockerDeviceResponse, DockerDevice
from app.utilities.load_config import load_config
from app.errors import NotExistImage, NotExistDevice


class DockerClient(DockerClient):
    _device_config: DeviceConfigForm

    def __init__(self, *args, **kwargs):
        self._device_config = load_config()
        super().__init__(*args, **kwargs)

    @classmethod
    def from_env(cls, *args, **kwargs) -> "DockerClient":
        return super().from_env(*args, **kwargs)

    async def delete_image(self, image_name):
        repository, tag = parse_repository_tag(image_name)
        async with aiohttp.ClientSession() as session:
            req = await session.get(
                f"http://localhost:5000/v2/{repository}/manifests/{tag if tag else "latest"}",
                headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
            )
            manifest = req.headers.get("Docker-Content-Digest")
            if req.status == 404:
                raise Exception("Not found image")
            if not req.ok:
                raise Exception(req.text)
            req = await session.delete(
                f"http://localhost:5000/v2/{repository}/manifests/{manifest}"
            )

            if not req.ok:
                raise Exception(req.text)

    def pull_image(self, image_name):
        image = self.images.pull(image_name)

        repository, tag = parse_repository_tag(image_name)
        repository = f"localhost:5000/{repository}"

        image.tag(repository, tag=tag)

        push_result = self.images.push(repository, tag=tag)
        logger.info(
            f"Pushed image to repository-{repository}, tag-{tag}. Result: {push_result}"
        )
        # try:
        #     image.remove(force=True)
        # except:
        #     pass

    def repull_image(self, image_name):
        self.pull_image(image_name)

    async def get_images(self) -> DockerImagesResponse:
        images = []
        async with aiohttp.ClientSession() as session:
            req = await session.get("http://localhost:5000/v2/_catalog")
            data = await req.json()
            repositories = data.get("repositories")

            for repository in repositories:
                req = await session.get(
                    f"http://localhost:5000/v2/{repository}/tags/list"
                )
                data = await req.json()
                images.append(data)
        return DockerImagesResponse(images=images)
    async def image_exists(self, image_name):
        repository, tag = parse_repository_tag(image_name)
        tag = tag if tag else "latest"


        images = await self.get_images()
        images = images.images

        image: list[DockerImage] = list(filter(lambda image: image.name == repository, images))

        if len(image) == 1:
            image: DockerImage = image[0]
        else:
            raise NotExistImage(image_name)

        tag = list(filter(lambda t: t == tag, image.tags))
        if not tag:
            raise NotExistImage(image_name)

    async def create_device(self, form: CreateDeviceForm, server_url):
        config = self._device_config.model_copy(deep=True)

        config.env.append(f"DEVICE_PHONE={form.name}")
        config.env.append(f"GATEWAY_URL={server_url}")

        self.services.create(form.image, name = form.name, **config.model_dump())

    def get_devices(self):
        services = self.services.list(filters={"label": "device"})
        response = DockerDeviceResponse(devices=[])

        for service in services:
            spec = service.attrs["Spec"]["TaskTemplate"]["ContainerSpec"]
            image = spec["Image"]
            env = spec["Env"]
            name = service.name
            server_url = list(filter(lambda x: "GATEWAY_URL=" in x, env))[0]
            server_url = server_url.replace("GATEWAY_URL=", "")
            response.devices.append(DockerDevice(name=name, env=env, image=image, server_url=server_url))


        return response

        # return DockerDeviceResponse(devices = [{"name": service.name} for service in services])

    def device_exists(self, device_name):
        devices = self.get_devices()
        device = list(filter(lambda d: d.name== device_name, devices.devices))
        if not device:
            raise NotExistDevice

    def delete_device(self, device_name):
        device = self.services.get(device_name)
        device.remove()
