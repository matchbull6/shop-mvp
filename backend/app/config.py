import os


def _require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Не задана переменная окружения {name}")
    return value


API_KEY = _require("API_KEY")
DATABASE_URL = _require("DATABASE_URL")
MINIO_URL = _require("MINIO_URL")
MINIO_ACCESS_KEY = _require("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = _require("MINIO_SECRET_KEY")
MINIO_BUCKET = _require("MINIO_BUCKET")

MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_NAME_LENGTH = 100
