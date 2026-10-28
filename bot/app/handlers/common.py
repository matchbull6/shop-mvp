from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message

from app import config
from app.handlers.admin import safe_delete
from app.keyboards import start_keyboard

router = Router(name="common")
router.message.filter(F.chat.type == ChatType.PRIVATE)

GREETING = "У меня есть товар, откройте каталог."


@router.message(CommandStart())
async def start(message: Message) -> None:
    is_admin = bool(message.from_user and message.from_user.id in config.ADMIN_IDS)
    await message.answer(GREETING, reply_markup=start_keyboard(is_admin))


@router.message()
async def delete_other(message: Message) -> None:
    await safe_delete(message)
