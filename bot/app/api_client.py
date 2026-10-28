import aiohttp


class ApiError(Exception):
    pass


class ApiClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self._session = aiohttp.ClientSession(
            base_url=base_url,
            headers={"X-API-Key": api_key},
            timeout=aiohttp.ClientTimeout(total=30),
            raise_for_status=True,
        )

    async def close(self) -> None:
        await self._session.close()

    async def create_product(self, name: str, image: bytes) -> None:
        form = aiohttp.FormData()
        form.add_field("name", name)
        form.add_field("image", image, filename="photo.jpg", content_type="image/jpeg")

        try:
            response = await self._session.post("/api/products", data=form)
            response.release()
        except (aiohttp.ClientError, TimeoutError) as exc:
            raise ApiError() from exc
