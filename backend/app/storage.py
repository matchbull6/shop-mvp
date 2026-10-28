import io
import uuid

from miniopy_async.api import Minio
from miniopy_async.error import S3Error


class ImageStorage:
    def __init__(self, client: Minio, bucket: str) -> None:
        self._client = client
        self._bucket = bucket

    async def ensure_bucket(self) -> None:
        try:
            await self._client.make_bucket(self._bucket)
        except S3Error as exc:
            if exc.code != "BucketAlreadyOwnedByYou":
                raise

    async def put(self, image_uuid: uuid.UUID, data: bytes) -> None:
        await self._client.put_object(
            self._bucket,
            str(image_uuid),
            io.BytesIO(data),
            length=len(data),
            content_type="image/jpeg",
        )

    async def get(self, image_uuid: uuid.UUID) -> bytes:
        response = await self._client.get_object(self._bucket, str(image_uuid))
        async with response:
            return await response.read()
