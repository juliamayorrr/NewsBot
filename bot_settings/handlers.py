from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from db_settings import db_funcs as db
from bot_settings import text as tx, keyboards as key, formatters as form

router = Router()

@router.message(Command(commands='start'))
async def process_start_command(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    username = message.from_user.username
    await message.answer(tx.start_command)
    await db.add_user(user_id=user_id,
                      username=username,
                      session=session)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=tx.help_command,
                         parse_mode='HTML')


@router.message(Command(commands='news'))
async def process_news_by_sources_command(message: Message):
    markup = key.get_sources_keyboard()
    await message.answer(text=tx.news_command,
                         reply_markup=markup)


@router.message(Command(commands='my_news'))
async def process_news_by_default_source_command(message: Message, session: AsyncSession):
    user_id = message.from_user.id

    news, status = await db.get_unread_news(
        session=session,
        user_id=user_id,
        source_id=None,
        use_default_source=True)

    if status == 'ok':
        answer = form.format_news_list(news=news)
    elif status == 'no_default_source':
        answer = tx.my_news_is_empty
    elif status == 'no_news':
        answer = tx.news_is_empty
    elif status == 'no_user':
        answer = tx.user_is_empty

    await message.answer(text=answer,
                         parse_mode='HTML')


@router.message(Command(commands='all_news'))
async def process_all_news_command(message: Message, session: AsyncSession):
    user_id = message.from_user.id

    news, status = await db.get_unread_news(
        session=session,
        user_id=user_id,
        source_id=None,
        use_default_source=False)

    if status == 'ok':
        answer = form.format_news_list(news=news)
    elif status == 'no_news':
        answer = tx.news_is_empty
    elif status == 'no_user':
        answer = tx.user_is_empty

    await message.answer(text=answer,
                         parse_mode='HTML')


@router.callback_query(F.data.startswith('news_source_'))
async def send_news_from_source(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    source_id = form.cut_id_from_callback(callback=callback)

    news, status = await db.get_unread_news(
        session=session,
        user_id=user_id,
        source_id = source_id,
        use_default_source=False)

    if status == 'ok':
        answer = form.format_news_list(news=news)
    elif status == 'no_news':
        answer = tx.news_is_empty
    elif status == 'no_user':
        answer = tx.user_is_empty

    await callback.message.answer(text=answer,
                                  parse_mode='HTML')
    await callback.answer()


@router.message(Command(commands='settings'))
async def process_settings_command(message: Message, session: AsyncSession):
    user_id = message.from_user.id

    user = await db.get_user(user_id=user_id,
                             session=session)
    answer = form.format_user_settings(user=user)
    markup = key.get_settings_keyboard()

    await message.answer(text=answer,
                         parse_mode='HTML',
                         reply_markup=markup)


@router.callback_query(F.data=='change_default_source')
async def change_default_source_handler(callback: CallbackQuery):
    markup = key.get_default_sources_keyboard()
    await callback.message.answer(text=tx.new_default_source,
                                  reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith('default_source_'))
async def change_default_source_process(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    source_id = form.cut_id_from_callback(callback=callback)

    await db.change_default_news_source(user_id=user_id,
                                     source_id=source_id,
                                     session=session)

    await callback.answer(tx.good_change_default_source)


@router.callback_query(F.data=='change_default_news_count')
async def change_default_news_count_handler(callback: CallbackQuery):
    markup = key.get_news_counts_keyboard()
    await callback.message.answer(text=tx.new_news_count,
                                  reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith('news_count_'))
async def change_default_news_count_process(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    news_count = form.cut_id_from_callback(callback=callback)

    await db.change_default_news_count(user_id=user_id,
                                     news_count=news_count,
                                     session=session)

    await callback.answer(tx.good_change_default_news_count)


@router.message(Command(commands='subscribes'))
async def process_subscribes_command(message: Message, session: AsyncSession):
    user_id = message.from_user.id

    user = await db.get_user(user_id=user_id,
                             session=session)

    answer = form.format_user_subscribes(user=user)
    markup = key.get_change_subscribes_keyboard()

    await message.answer(text=answer,
                         parse_mode='HTML',
                         reply_markup=markup)


@router.callback_query(F.data=='subscribe')
async def subscribe_to_source_handler(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    user = await db.get_user(user_id=user_id,
                             session=session)
    sub_sources = [source.id for source in user.subscribed_sources]
    markup = key.get_subscribe_sources_keyboard(sub_sources=sub_sources)
    await callback.message.answer(text=tx.change_sources_to_subscribe,
                                  reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith('subscribe_news_source_'))
async def subscribe_to_source_process(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    subscribe_source_id = form.cut_id_from_callback(callback=callback)

    await db.add_new_subscribe(user_id=user_id,
                               subscribe_source_id=subscribe_source_id,
                               session=session)

    await callback.answer(tx.good_change_sources_to_subscribe)


@router.callback_query(F.data=='cancel_subscribe')
async def cancel_subscribe_to_source_handler(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    user = await db.get_user(user_id=user_id,
                             session=session)
    sub_sources = [source.id for source in user.subscribed_sources]
    markup = key.get_cancel_subscribe_sources_keyboard(sub_sources=sub_sources)
    await callback.message.answer(text=tx.change_sources_to_cancel_subscribe,
                                  reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith('cancel_subscribe_news_source_'))
async def cancel_subscribe_to_source_process(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    subscribe_source_id = form.cut_id_from_callback(callback=callback)

    await db.cancel_subscribe(user_id=user_id,
                               subscribe_source_id=subscribe_source_id,
                               session=session)

    await callback.answer(tx.good_cancel_subscribe)
