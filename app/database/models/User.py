from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.auth.utils import hash_password
from app.errors import AlreadyExistsInDB, UserAlreadyExist
from app.schemas import CreateUserForm, UserRoleEnum

from .__Base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum), nullable=False
    )

    def __init__(self, form: CreateUserForm):
        self.username = form.username
        self.password_hash = hash_password(form.password)
        self.role = form.role

    @classmethod
    def exists(cls, username: str):
        try:
            super().exists(cls.username == username)
        except AlreadyExistsInDB:
            raise UserAlreadyExist(username)
