import asyncio
from aiogram import Bot, Dispatcher
from bot_settings import handlers, menu
import config
from db_settings.db_funcs import load_sources_to_cache, add_to_db_and_autosend_news, add_news
from db_settings.db_middleware import DataBaseSession
from db_settings.engine import session_maker
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def main():
    bot = Bot(token=config.Bot.token)
    dp = Dispatcher()

    dp.include_router(handlers.router)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    config.NewsAPI.sources = await load_sources_to_cache()

    await add_news()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(func=add_to_db_and_autosend_news,
                      trigger='interval',
                      hours=config.NewsAPI.interval_to_fetch,
                      args=[bot])
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())