import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app import config
from app.api_client import ApiClient
from app.handlers import admin, common
from app.keyboards import menu_button


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    dispatcher["api"] = ApiClient(config.API_URL, config.API_KEY)

    await bot.set_chat_menu_button(menu_button=menu_button())

    for _ in range(5):
        try:
            await bot.set_webhook(
                url=config.WEBHOOK_URL,
                secret_token=config.WEBHOOK_SECRET,
                allowed_updates=dispatcher.resolve_used_update_types(),
            )
            return
        except TelegramRetryAfter as exc:
            await asyncio.sleep(exc.retry_after)
    raise RuntimeError("Не удалось установить вебхук")


async def on_shutdown(dispatcher: Dispatcher) -> None:
    api: ApiClient = dispatcher["api"]
    await api.close()


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
    dispatcher.include_routers(admin.router, common.router)
    return dispatcher


def run_webhook(bot: Bot, dispatcher: Dispatcher) -> None:
    app = web.Application()

    SimpleRequestHandler(
        bot=bot,
        dispatcher=dispatcher,
        secret_token=config.WEBHOOK_SECRET,
    ).register(app, path=config.WEBHOOK_PATH)

    setup_application(app, dispatcher, bot=bot)
    web.run_app(app, host="0.0.0.0", port=config.PORT)


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = create_dispatcher()
    run_webhook(bot, dispatcher)


if __name__ == "__main__":
    main()
