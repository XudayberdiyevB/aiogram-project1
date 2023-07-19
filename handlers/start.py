from aiogram import types

from keyboards.regions import regions_btn
from main import dp


# @dp.message_handler(CommandStart)
@dp.message_handler(commands=["start"])
async def start_command_handler(message: types.Message):
    full_name = message.from_user.full_name
    await message.answer(f"Welcome to our bot {full_name}")
