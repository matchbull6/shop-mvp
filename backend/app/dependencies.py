from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import config
from app.repository import ProductRepository
from app.services import ProductService
from app.storage import ImageStorage


def require_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key is None or x_api_key != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный API-ключ"
        )


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    session_factory = request.app.state.session_factory
    async with session_factory() as session:
        yield session


def get_storage(request: Request) -> ImageStorage:
    return request.app.state.storage


def get_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    storage: Annotated[ImageStorage, Depends(get_storage)],
) -> ProductService:
    return ProductService(ProductRepository(session), storage)


Service = Annotated[ProductService, Depends(get_service)]
