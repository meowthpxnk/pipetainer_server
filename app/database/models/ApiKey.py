import secrets

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.errors import AlreadyExistsInDB, ApiKeyAlreadyexist
from app.schemas import CreateApiKeyForm

from .__Base import Base


class ApiKey(Base):
    __tablename__ = "api_key"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    key: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, form: CreateApiKeyForm):
        self.name = form.name
        self.key = secrets.token_hex(64)

    @classmethod
    def exists(cls, name: str):
        try:
            super().exists(cls.name == name)
        except AlreadyExistsInDB:
            raise ApiKeyAlreadyexist(name)
