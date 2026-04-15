from aiohttp import ClientSession
import config


class NewsAPIClient:
    def __init__(self):
        self.api_key = config.NewsAPI.api_key
        self.base_url = config.NewsAPI.base_url

    async def fetch_news(self, news_mode=None, q=None, sources=None):
        if news_mode not in config.NewsAPI.news_modes:
            news_mode = 'all'
        if q is None:
            q = 'finance OR investing OR trading OR финансы OR трейдинг OR инвестиции'
        if sources is None:
            sources = ','.join(config.NewsAPI.sources.keys())

        url = f"{self.base_url}{config.NewsAPI.news_modes[news_mode]}"
        params = {
            'q': q,
            'sources': sources,
            'apiKey': self.api_key,
        }
        async with ClientSession() as session:
            async with session.get(url=url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('articles', [])
                else:
                    error_text = await response.text()
                    print(f"Ошибка API: {response.status} - {error_text}")
                    return []