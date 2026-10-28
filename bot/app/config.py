import os


def _require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Не задана переменная окружения {name}")
    return value


BOT_TOKEN = _require("BOT_TOKEN")
ADMIN_IDS = [int(i) for i in os.getenv("ADMIN_IDS", "").split(",") if i.strip()]

WEBHOOK_SECRET = _require("WEBHOOK_SECRET")
WEBHOOK_PATH = _require("WEBHOOK_PATH")
WEBHOOK_URL = _require("WEBHOOK_HOST").rstrip("/") + WEBHOOK_PATH

WEBAPP_URL = _require("WEBAPP_URL")
API_URL = _require("API_URL")
API_KEY = _require("API_KEY")
PORT = int(_require("PORT"))

MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_NAME_LENGTH = 100
