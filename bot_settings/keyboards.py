from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config
from bot_settings import text as tx


def get_default_sources_keyboard() -> InlineKeyboardMarkup:
    """Создает и возвращает клавиатуру для управления новостным источником по умолчанию"""

    buttons = [[InlineKeyboardButton(text=domain,callback_data=f'default_source_{db_id}')]
                for domain, db_id in config.NewsAPI.sources.items()]

    buttons.append([InlineKeyboardButton(text=tx.button_clean_default_source,
                                         callback_data=f'default_source_0')])

    sources_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return sources_keyboard


def get_change_subscribes_keyboard() -> InlineKeyboardMarkup:
    """Создает и возвращает клавиатуру для управления подписками на источники"""

    buttons = [[InlineKeyboardButton(text=tx.button_subscribe_to_new_sources,
                                     callback_data='subscribe')],
              [InlineKeyboardButton(text=tx.button_cancel_subscribes,
                                     callback_data='cancel_subscribe')]]

    change_subscribes_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return change_subscribes_keyboard


def get_sources_keyboard() -> InlineKeyboardMarkup:
    """Создает и возвращает клавиатуру для выбора источника новостей"""

    buttons = [[InlineKeyboardButton(text=domain,callback_data=f'news_source_{db_id}')]
                for domain, db_id in config.NewsAPI.sources.items()]

    sources_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return sources_keyboard


def get_subscribe_sources_keyboard(sub_sources: list) -> InlineKeyboardMarkup:
    """Создает и возвращает клавиатуру для подписки на новый новостной источник"""

    buttons = [[InlineKeyboardButton(text=domain,callback_data=f'subscribe_news_source_{db_id}')]
                for domain, db_id in config.NewsAPI.sources.items() if db_id not in sub_sources]

    sources_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return sources_keyboard


def get_cancel_subscribe_sources_keyboard(sub_sources: list) -> InlineKeyboardMarkup:
    """Создает и возвращает клавиатуру для отмены подписки на новостной источник"""

    buttons = [[InlineKeyboardButton(text=domain, callback_data=f'cancel_subscribe_news_source_{db_id}')]
               for domain, db_id in config.NewsAPI.sources.items() if db_id in sub_sources]

    sub_sources_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return sub_sources_keyboard


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Создает и возвращает клавиатуру для управления настройками получения новостей"""

    buttons = [[InlineKeyboardButton(text=tx.button_change_default_news_source,
                                     callback_data='change_default_source')],
              [InlineKeyboardButton(text=tx.button_change_default_news_count,
                                     callback_data='change_default_news_count')]]

    settings_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return settings_keyboard


def get_news_counts_keyboard() -> InlineKeyboardMarkup:
    """Создает и возвращает клавиатуру для управления количеством получаемых новостей за раз"""

    news_counts = (1, 5, 10, 15, 20, 30)

    buttons = [[InlineKeyboardButton(text=f'{count}', callback_data=f'news_count_{count}')]
                for count in news_counts]

    counts_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return counts_keyboard