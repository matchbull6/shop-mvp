import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Response,
    UploadFile,
    status,
)

from app import config
from app.dependencies import Service, require_api_key
from app.schemas import ProductOut, ProductPage
from app.services import ValidationError

router = APIRouter(prefix="/api")


@router.get("/products")
async def get_products(
    service: Service,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> ProductPage:
    items, total = await service.get_products(limit, offset)
    return ProductPage(items=[ProductOut.from_model(p) for p in items], total=total)


@router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
async def create_product(
    service: Service,
    name: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
) -> ProductOut:
    data = await image.read(config.MAX_IMAGE_SIZE + 1)
    try:
        product = await service.create_product(name, data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
        ) from exc
    return ProductOut.from_model(product)


@router.get("/images/{image_uuid}")
async def get_image(service: Service, image_uuid: uuid.UUID) -> Response:
    data = await service.get_image(image_uuid)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Изображение не найдено"
        )
    return Response(
        content=data,
        media_type="image/jpeg",
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )