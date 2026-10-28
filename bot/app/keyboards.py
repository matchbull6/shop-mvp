from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    WebAppInfo,
)

from app import config

BTN_WEBAPP = "Открыть каталог"
BTN_CREATE_PRODUCT = "Создать товар"
CB_CREATE_PRODUCT = "create_product"

WEB_APP = WebAppInfo(url=config.WEBAPP_URL)


def start_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    row = [InlineKeyboardButton(text=BTN_WEBAPP, web_app=WEB_APP)]
    if is_admin:
        row.append(
            InlineKeyboardButton(
                text=BTN_CREATE_PRODUCT, callback_data=CB_CREATE_PRODUCT
            )
        )
    return InlineKeyboardMarkup(inline_keyboard=[row])


def menu_button() -> MenuButtonWebApp:
    return MenuButtonWebApp(text=BTN_WEBAPP, web_app=WEB_APP)
