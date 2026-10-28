import uuid

from app import config
from app.models import Product
from app.repository import ProductRepository
from app.storage import ImageStorage

JPEG_SIGNATURE = b"\xff\xd8\xff"


class ValidationError(Exception):
    pass


class ProductService:
    def __init__(self, repo: ProductRepository, storage: ImageStorage) -> None:
        self._repo = repo
        self._storage = storage

    async def get_products(self, limit: int, offset: int) -> tuple[list[Product], int]:
        items = await self._repo.list(limit, offset)
        total = await self._repo.count()
        return items, total

    async def create_product(self, name: str, image: bytes) -> Product:
        name = name.strip()

        if not name:
            raise ValidationError("Название не может быть пустым.")
        if len(name) > config.MAX_NAME_LENGTH:
            raise ValidationError(
                f"Название длиннее {config.MAX_NAME_LENGTH} символов."
            )
        if len(image) > config.MAX_IMAGE_SIZE:
            raise ValidationError(
                f"Фото больше {config.MAX_IMAGE_SIZE // (1024 * 1024)} МБ."
            )
        if not image.startswith(JPEG_SIGNATURE):
            raise ValidationError("Поддерживается только JPEG.")

        image_uuid = uuid.uuid4()
        await self._storage.put(image_uuid, image)
        return await self._repo.add(name, image_uuid)

    async def get_image(self, image_uuid: uuid.UUID) -> bytes | None:
        return await self._storage.get(image_uuid)
