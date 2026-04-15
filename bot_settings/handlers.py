from aiogram import Router
from aiogram.filters import Command

router = Router()

@router.message(Command(commands='start'))
async def process_start_command(message, session):
    await message.answer('Привет')