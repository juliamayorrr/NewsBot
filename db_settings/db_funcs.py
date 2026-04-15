import config
from db_settings.engine import session_maker
from db_settings.models import News, NewsSources
from news_collectors.news_api import NewsAPIClient
from sqlalchemy import select


async def load_sources_to_cache():
    async with session_maker() as session:
        result = await session.execute(select(NewsSources))
        sources = result.scalars().all()
        sources_dict = {source.api_id: source.id for source in sources}
        return sources_dict


async def add_news():
    client = NewsAPIClient()
    raw_news = await client.fetch_news()

    async with session_maker() as session:
        sources = config.NewsAPI.sources
        news = []
        for item in raw_news:
            source_id = sources[item['source']['id']]
            news.append(News(
                source_id=source_id,
                title=item['title'],
                url=item['url']
            ))

        session.add_all(news)
        await session.commit()


