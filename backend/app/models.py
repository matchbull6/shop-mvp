import uuid

from sqlalchemy import String, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app import config


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(config.MAX_NAME_LENGTH))
    image_uuid: Mapped[uuid.UUID] = mapped_column(Uuid, unique=True)
