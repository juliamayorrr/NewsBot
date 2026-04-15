import asyncio
from aiogram import Bot, Dispatcher
from bot_settings import handlers, menu
import config
from db_settings.db_funcs import add_news, load_sources_to_cache
from db_settings.db_middleware import DataBaseSession
from db_settings.engine import session_maker
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def main():
    bot = Bot(token=config.Bot.token)
    dp = Dispatcher()

    dp.include_router(handlers.router)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await menu.set_menu(bot)

    config.NewsAPI.sources = await load_sources_to_cache()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(func=add_news,
                      trigger='interval',
                      hours=12)
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())