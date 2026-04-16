from aiogram import Bot
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import config
from db_settings.engine import session_maker
from db_settings.models import News, NewsSources, SentNews
from news_collectors.news_api import NewsAPIClient
from sqlalchemy import select
from typing import Sequence
from db_settings.models import Users, News, NewsSources
from bot_settings import text as tx, formatters as form


async def load_sources_to_cache() -> dict:
    """Генерирует словарь, где ключами являются домены новостных ресурсов,
     а значениями - их id в БД для быстрого доступа к этим данным"""

    async with session_maker() as session:
        result = await session.execute(select(NewsSources))
        sources = result.scalars().all()
        sources_dict = {source.domain: source.id for source in sources}
        return sources_dict


async def add_news() -> None:
    """Добавляет новости, полученные через API, в базу данных"""

    client = NewsAPIClient()
    raw_news = await client.fetch_news()

    async with session_maker() as session:
        result = await session.execute(select(News.url))
        existing_urls = set(result.scalars().all())

        sources = config.NewsAPI.sources
        news = []
        for item in raw_news:
            for domain, db_id in sources.items():
                if domain in item['url']:
                    source_id = db_id
                    break
            else:
                continue

            if item['url'] not in existing_urls:
                news.append(News(
                    source_id=source_id,
                    title=item['title'],
                    url=item['url']
                ))

        session.add_all(news)
        await session.commit()


async def send_news_to_subscribers(bot: Bot) -> None:
    """Рассылает новости из всех источников подписанным пользователям"""

    async with (session_maker() as session):
        result = await session.execute(select(Users
        ).options(
        selectinload(Users.subscribed_sources)
        ).where(
            Users.subscribed_sources.any()
        ))
        users = result.scalars().all()

        for user in users:
            for source in user.subscribed_sources:
                news = await get_unread_news(
                    session=session,
                    user_id=user.id,
                    source_id=source.id,
                    use_default_source=False)

                head = f'Новости по подписке на {source.domain}\n\n'
                if news:
                    answer = head + form.format_news_list(news)
                else:
                    answer = head + tx.news_is_empty

                await bot.send_message(chat_id=user.id,
                                       text=answer,
                                       parse_mode='HTML')


async def add_to_db_and_autosend_news(bot: Bot) -> None:
    """Запускает сбор новостей из API, добавление их в БД и рассылку подписанным пользователям"""

    await add_news()
    await send_news_to_subscribers(bot=bot)


async def add_user(user_id: int, username: str, session: AsyncSession) -> None:
    """Добавляет пользователя в БД"""

    user = Users(
        id=user_id,
        username=username
        )
    try:
        session.add(user)
        await session.commit()
    except IntegrityError:
        print('Команда /start от существующего пользователя')


async def get_user(user_id: int, session: AsyncSession):
    """Возвращает запись пользователя из БД"""

    user = await session.get(Users, user_id, options=[selectinload(Users.default_news_source),
                                                      selectinload(Users.subscribed_sources)])

    return user


async def add_news_to_sent_news(user_id: int, news: Sequence[News], session: AsyncSession):
    """Добавляет новости в таблицу отправленных новостей для конкретного пользователя"""

    for item in news:
        session.add(SentNews(user_id=user_id, news_id=item.id))

    await session.commit()


async def get_unread_news(
        session: AsyncSession,
        user_id: int,
        source_id: int = None,
        use_default_source: bool = False) -> Sequence[News]:
    """Универсальная функция получения непрочитанных новостей - по одному источнику,
    по всем источникам, по дефолтному источнику"""

    user = await get_user(user_id=user_id,
                          session=session)
    if not user:
        return []

    if use_default_source:
        if not user.default_news_source:
            return []
        source_id = user.default_news_source.id

    subq = select(SentNews.news_id).where(SentNews.user_id == user_id)

    query = select(News).options(selectinload(News.source))

    if source_id is not None:
        query = query.where(News.source_id == source_id)

    query = query.where(News.id.not_in(subq))
    query = query.order_by(News.created.desc()).limit(user.default_news_count)

    result = await session.execute(query)
    news = result.scalars().all()

    await add_news_to_sent_news(user_id, news, session)
    await session.commit()

    return news


async def change_default_news_source(user_id: int, source_id: int, session: AsyncSession):
    """Меняет источник новостей по умолчанию у конкретного пользователя"""

    user = await get_user(user_id=user_id,
                          session=session)
    if source_id:
        user.default_news_source_id = source_id
    else:
        user.default_news_source_id = None
    await session.commit()


async def change_default_news_count(user_id: int, news_count: int, session: AsyncSession):
    """Меняет количество выдаваемых новостей по умолчанию у конкретного пользователя"""

    user = await get_user(user_id=user_id,
                          session=session)

    user.default_news_count = news_count

    await session.commit()


async def add_new_subscribe(user_id: int, subscribe_source_id: int, session: AsyncSession):
    """Добавляет новостной ресурс в подписки пользователя"""

    user = await get_user(user_id=user_id,
                          session=session)

    source = await session.get(NewsSources, subscribe_source_id)

    user.subscribed_sources.add(source)

    await session.commit()