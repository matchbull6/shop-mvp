import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, name: str, image_uuid: uuid.UUID) -> Product:
        product = Product(name=name, image_uuid=image_uuid)
        self._session.add(product)
        await self._session.commit()
        await self._session.refresh(product)
        return product

    async def get(self, product_id: int) -> Product | None:
        return await self._session.get(Product, product_id)

    async def list(self, limit: int, offset: int) -> list[Product]:
        query = select(Product).order_by(Product.id.desc()).limit(limit).offset(offset)
        result = await self._session.scalars(query)
        return list(result)

    async def count(self) -> int:
        return (
            await self._session.scalar(select(func.count()).select_from(Product)) or 0
        )
