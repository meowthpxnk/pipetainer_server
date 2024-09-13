from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.errors import AlreadyExistsInDB, ServerAlreadyExist
from app.schemas import CreateServerForm

from .__Base import Base


class Server(Base):
    __tablename__ = "server"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_name: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    url: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, form: CreateServerForm):
        self.short_name = form.short_name
        self.url = form.url

    @classmethod
    def exists(cls, short_name: str):
        try:
            super().exists(cls.short_name == short_name)
        except AlreadyExistsInDB:
            raise ServerAlreadyExist(short_name)
