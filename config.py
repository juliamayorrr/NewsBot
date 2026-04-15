import os
import dotenv


dotenv.load_dotenv()

class Bot:
    token = os.getenv('BOT_TOKEN')

class Database:
    name = os.getenv('POSTGRES_DB')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    url = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}'

class NewsAPI:
    api_key = os.getenv('NEWSAPI_KEY')
    base_url = "https://newsapi.org/v2"
    news_modes = {'all': '/everything',
                  'top': '/top-headlines'
                  }
    sources = None