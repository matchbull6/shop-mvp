from pydantic import BaseModel

from app.models import Product


class ProductOut(BaseModel):
    id: int
    name: str
    image_url: str

    @classmethod
    def from_model(cls, product: Product) -> "ProductOut":
        return cls(
            id=product.id,
            name=product.name,
            image_url=f"/api/images/{product.image_uuid}",
        )


class ProductPage(BaseModel):
    items: list[ProductOut]
    total: int
