import asyncio
from aiogram import Bot, Dispatcher
from bot_settings import config, handlers, menu
from db_settings.db_middleware import DataBaseSession
from db_settings.engine import session_maker


async def main():
    bot = Bot(token=config.Bot.token)
    dp = Dispatcher()

    dp.include_router(handlers.router)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await menu.set_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())