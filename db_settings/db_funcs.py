import config
from db_settings.engine import session_maker
from db_settings.models import News, NewsSources
from news_collectors.news_api import NewsAPIClient
from sqlalchemy import select


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
        sources = config.NewsAPI.sources
        news = []
        for item in raw_news:
            for domain, db_id in sources.items():
                if domain in item['url']:
                    source_id = db_id
                    break
            else:
                continue

            news.append(News(
                source_id=source_id,
                title=item['title'],
                url=item['url']
            ))

        session.add_all(news)
        await session.commit()


