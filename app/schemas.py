import enum
from typing import Optional

from pydantic import BaseModel, RootModel


class UserRoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    SUPPORT = "SUPPORT"

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Other must be Role type.")

        match self.value:
            case "ADMIN":
                if other.value == "ADMIN":
                    return False
                elif other.value == "SUPERVISOR":
                    return False
                elif other.value == "SUPPORT":
                    return False
            case "SUPERVISOR":
                if other.value == "ADMIN":
                    return True
                elif other.value == "SUPERVISOR":
                    return False
                elif other.value == "SUPPORT":
                    return False
            case "SUPPORT":
                if other.value == "ADMIN":
                    return True
                elif other.value == "SUPERVISOR":
                    return True
                elif other.value == "SUPPORT":
                    return False

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Other must be Role type.")

        match self.value:
            case "ADMIN":
                if other.value == "ADMIN":
                    return True
                elif other.value == "SUPERVISOR":
                    return False
                elif other.value == "SUPPORT":
                    return False
            case "SUPERVISOR":
                if other.value == "ADMIN":
                    return True
                elif other.value == "SUPERVISOR":
                    return True
                elif other.value == "SUPPORT":
                    return False
            case "SUPPORT":
                if other.value == "ADMIN":
                    return True
                elif other.value == "SUPERVISOR":
                    return True
                elif other.value == "SUPPORT":
                    return True

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Other must be Role type.")

        match self.value:
            case "ADMIN":
                if other.value == "ADMIN":
                    return False
                elif other.value == "SUPERVISOR":
                    return True
                elif other.value == "SUPPORT":
                    return True
            case "SUPERVISOR":
                if other.value == "ADMIN":
                    return False
                elif other.value == "SUPERVISOR":
                    return False
                elif other.value == "SUPPORT":
                    return True
            case "SUPPORT":
                if other.value == "ADMIN":
                    return False
                elif other.value == "SUPERVISOR":
                    return False
                elif other.value == "SUPPORT":
                    return False

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Other must be Role type.")

        match self.value:
            case "ADMIN":
                if other.value == "ADMIN":
                    return True
                elif other.value == "SUPERVISOR":
                    return True
                elif other.value == "SUPPORT":
                    return True
            case "SUPERVISOR":
                if other.value == "ADMIN":
                    return False
                elif other.value == "SUPERVISOR":
                    return True
                elif other.value == "SUPPORT":
                    return True
            case "SUPPORT":
                if other.value == "ADMIN":
                    return False
                elif other.value == "SUPERVISOR":
                    return False
                elif other.value == "SUPPORT":
                    return True


class LoggerLevel(enum.Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"


class JWTTokenTypeEnum(enum.Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class AuthForm(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    role: UserRoleEnum


class FetchPayloadSchema(User):
    pass


class CreateUserForm(User):
    password: str


class ApiKey(BaseModel):
    name: str


class CreateApiKeyForm(ApiKey):
    pass


class PullImageForm(BaseModel):
    image_name: str


class DockerLoginForm(BaseModel):
    username: str
    password: str


class Server(BaseModel):
    short_name: str
    url: str


class CreateServerForm(Server):
    pass


class TokenPayloadSchema(User):
    session_id: str


class DockerImage(BaseModel):
    name: str
    tags: Optional[list[str]] = None


class DockerDevice(BaseModel):
    name: str
    env: list[str]
    image: str
    server_url: str


class DockerImagesResponse(BaseModel):
    images: list[DockerImage]


class DockerDeviceResponse(BaseModel):
    devices: list[DockerDevice]


class ImageSchema(BaseModel):
    image_name: str


class TokenDataSchema(TokenPayloadSchema):
    exp: int
    type: JWTTokenTypeEnum


class Device(BaseModel):
    name: str
    image: str
    server_short_name: str


class CreateDeviceForm(Device):
    pass


class DeviceConfigForm(BaseModel):
    labels: dict[str, str]
    env: list[str]
    networks: list[str]
    mounts: list[str]


class DeviceStatus(enum.Enum):
    LOST_REGISTRATION = "LOST_REGISTRATION"
    ONLINE = "ONLINE"
    FAILED = "FAILED"


class DeviceQRRequest(BaseModel):
    data_ref: str


class DeviceStatusRequest(BaseModel):
    status: DeviceStatus


class WebsocketResponseDeviceData(BaseModel):
    status: Optional[DeviceStatus] = None
    qr: Optional[str] = None


class WebsocketResponse(BaseModel):
    device_name: str
    data: WebsocketResponseDeviceData


class WebsocketRootConnection(BaseModel):
    root: bool = True
    data: list[WebsocketResponse] = []
