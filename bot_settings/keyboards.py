from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config


def get_default_sources_keyboard():
    buttons = [[InlineKeyboardButton(text=domain,callback_data=f'default_source_{db_id}')]
                for domain, db_id in config.NewsAPI.sources.items()]
    buttons.append([InlineKeyboardButton(text='Очистить источник по умолчанию',
                                         callback_data=f'default_source_0')])
    sources_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return sources_keyboard


def get_subscribed_sources_keyboard(sources):
    buttons = [[InlineKeyboardButton(text=source.domain,callback_data=f'subscribed_source_{source.id}')]
                for source in sources]

    sub_sources_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return sub_sources_keyboard


def get_change_subscribes_keyboard():
    change_subscribes_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Подписаться на новые источники',
                                               callback_data='subscribe')],
                         [InlineKeyboardButton(text='Отписаться от источников',
                                               callback_data='cancel_subscribe')]])
    return change_subscribes_keyboard


def get_sources_keyboard():
    sources_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text=domain,callback_data=f'news_source_{db_id}')]
                    for domain, db_id in config.NewsAPI.sources.items()
                    ])
    return sources_keyboard


def get_subscribe_sources_keyboard():
    sources_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text=domain,callback_data=f'subscribe_news_source_{db_id}')]
                    for domain, db_id in config.NewsAPI.sources.items()
                    ])
    return sources_keyboard


def get_cancel_subscribe_sources_keyboard():
    sources_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text=domain,callback_data=f'cancel_subscribe_news_source_{db_id}')]
                    for domain, db_id in config.NewsAPI.sources.items()
                    ])
    return sources_keyboard


def get_settings_keyboard():
    settings_keyboard = InlineKeyboardMarkup(
                        inline_keyboard=[[InlineKeyboardButton(text='Изменить источник по умолчанию',
                                            callback_data='change_default_source')],
                        [InlineKeyboardButton(text='Изменить количество новостей по умолчанию',
                                            callback_data='change_default_news_count')]])
    return settings_keyboard


def get_news_counts_keyboard():
    news_counts = (1, 5, 10, 15, 20, 30)

    counts_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text=f'{count}', callback_data=f'news_count_{count}')]
                    for count in news_counts
                    ])
    return counts_keyboard