from aiogram.types import BotCommand

async def set_menu(bot):
    menu_commands = [
        BotCommand(
            command='/help',
            description='Справка по работе бота'),
        BotCommand(
            command='/news',
            description='Просмотр новостей по источникам'),
        BotCommand(
            command='/all_news',
            description='Новости из всех источников'),
        BotCommand(
            command='/my_news',
            description='Новости из вашего источника по умолчанию'),
        BotCommand(
            command='/settings',
            description='Настройка параметров получения новостей'),
        BotCommand(
            command='/subscribes',
            description='Управление подписками на новости'),
    ]
    await bot.set_my_commands(menu_commands)