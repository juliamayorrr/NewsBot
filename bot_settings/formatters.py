from typing import Sequence
from db_settings.models import News, Users


def format_news_list(news: Sequence[News]) -> str:
    news_list = ''

    for item in news:
        news_list += (f'{item.title}\n'
                      f"<a href='{item.url}'>{item.source.domain}</a>\n\n")

    return news_list

def format_user_settings(user: Users) -> str:
    default_source = user.default_news_source.domain if user.default_news_source else 'Не задан'
    user_settings = (f'Ваш источник новостей по умолчанию: {default_source}\n\n'
                     f'Ваше количество новостей по умолчанию: {user.default_news_count}')

    return user_settings