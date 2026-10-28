import asyncio
import io
from contextlib import suppress
from html import escape
from typing import Any

from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, ForceReply, Message, PhotoSize

from app import config
from app.api_client import ApiClient, ApiError
from app.keyboards import CB_CREATE_PRODUCT

router = Router(name="admin")
router.message.filter(F.chat.type == ChatType.PRIVATE)

FILTER_PHOTO = F.photo[-1].as_("photo")
FILTER_NAME = F.caption.func(str.strip).as_("name")
FILTER_IS_ADMIN = F.from_user.id.in_(config.ADMIN_IDS)

HINT = "Ответьте на это сообщение: фото товара и его название в подписи."
HINT_TTL = 60
RESULT_TTL = 10


def reply_to_hint(message: Message, bot: Bot) -> bool | dict[str, Any]:
    replied = message.reply_to_message
    if (
        replied
        and replied.from_user
        and replied.from_user.id == bot.id
        and replied.text
        and replied.text.endswith(HINT)
    ):
        return {"hint": replied}
    return False


async def safe_delete(message: Message) -> None:
    with suppress(TelegramBadRequest):
        await message.delete()


async def notify(
    bot: Bot,
    chat_id: int,
    text: str,
    delay: float = RESULT_TTL,
    reply_markup: ForceReply | None = None,
) -> None:
    sent = await bot.send_message(chat_id, text, reply_markup=reply_markup)
    await asyncio.sleep(delay)
    await safe_delete(sent)


async def send_hint(bot: Bot, chat_id: int, error: str | None = None) -> None:
    text = f"{error}\n\n{HINT}" if error else HINT
    await notify(bot, chat_id, text, delay=HINT_TTL, reply_markup=ForceReply())


async def replace_hint(
    message: Message, hint: Message, bot: Bot, error: str | None = None
) -> None:
    await safe_delete(message)
    await safe_delete(hint)
    await send_hint(bot, message.chat.id, error)


@router.callback_query(F.data == CB_CREATE_PRODUCT, FILTER_IS_ADMIN)
async def create_clicked(callback: CallbackQuery, bot: Bot) -> None:
    await callback.answer()
    await send_hint(bot, callback.from_user.id)


@router.callback_query(F.data == CB_CREATE_PRODUCT)
async def create_no_rights(callback: CallbackQuery) -> None:
    await callback.answer("Недостаточно прав.", show_alert=True)


@router.message(FILTER_IS_ADMIN, reply_to_hint, FILTER_PHOTO, FILTER_NAME)
async def create_product(
    message: Message,
    hint: Message,
    bot: Bot,
    api: ApiClient,
    name: str,
    photo: PhotoSize,
) -> None:
    if len(name) > config.MAX_NAME_LENGTH:
        error = f"Название длиннее {config.MAX_NAME_LENGTH} символов."
        await replace_hint(message, hint, bot, error)
        return
    if photo.file_size and photo.file_size > config.MAX_IMAGE_SIZE:
        error = f"Фото больше {config.MAX_IMAGE_SIZE // (1024 * 1024)} МБ."
        await replace_hint(message, hint, bot, error)
        return

    buffer = io.BytesIO()
    await bot.download(photo, destination=buffer)

    await safe_delete(hint)
    await safe_delete(message)

    try:
        await api.create_product(name, image=buffer.getvalue())
    except ApiError:
        await notify(bot, message.chat.id, "Возникла ошибка, попробуйте ещё раз.")
        return

    await notify(bot, message.chat.id, f"Товар <b>{escape(name)}</b> создан.")


@router.message(FILTER_IS_ADMIN, reply_to_hint)
async def invalid_reply(message: Message, hint: Message, bot: Bot) -> None:
    if message.media_group_id is not None:
        await safe_delete(message)
        return

    await replace_hint(message, hint, bot)
