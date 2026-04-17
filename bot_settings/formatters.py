from typing import Sequence
from aiogram.types import CallbackQuery
from db_settings.models import News, Users


def cut_id_from_callback(callback: CallbackQuery) -> int:
    """Извлекает id из текста CallbackQuery"""

    return int(callback.data.split('_')[-1])


def format_news_list(news: Sequence[News]) -> str:
    """Форматирует список новостей в текст для отправки пользователю"""

    news_list = ''

    for item in news:
        news_list += (f'<u>{item.published_at.date()}</u>\n'
                      f'{item.title}\n'
                      f"<a href='{item.url}'>{item.source.domain}</a>\n\n")

    return news_list


def format_user_settings(user: Users) -> str:
    """Форматирует настройки новостей пользователя в текст для отправки пользователю"""

    default_source = user.default_news_source.domain if user.default_news_source else 'Не задан'
    user_settings = (f'Ваш источник новостей по умолчанию: {default_source}\n\n'
                     f'Ваше количество отправляемых новостей по умолчанию: {user.default_news_count}')

    return user_settings


def format_user_subscribes(user: Users) -> str:
    """Форматирует новостные подписки пользователя в текст для отправки пользователю"""

    subs_list = ', '.join([source.domain for source in user.subscribed_sources]) if user.subscribed_sources \
        else 'У вас нет подписок'

    subs = f'Ваши подписки: {subs_list}'

    return subs