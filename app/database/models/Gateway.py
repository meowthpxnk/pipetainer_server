from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .__Base import Base


class Gateway(Base):
    __tablename__ = "gateway"
    id: Mapped[int] = mapped_column(primary_key=True)
    gateway_url: Mapped[str] = mapped_column(String)
    short_name: Mapped[str] = mapped_column(String)
