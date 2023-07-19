import logging

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from db.config import connection
from keyboards.regions import regions_inline_btn, get_cities_btn
from settings import BOT_TOKEN
from states.register import RegisterForm

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def start_command_handler(message: types.Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    with connection.cursor() as cursor:
        cursor.execute("select chat_id from users")
        chat_ids = cursor.fetchall()
        if chat_id not in [id_[0] for id_ in chat_ids]:
            cursor.execute("insert into users(chat_id, full_name) values (%s, %s)", (chat_id, full_name))
            connection.commit()
    await message.answer(f"Welcome to our bot {full_name}")
    # await message.answer(f"Please select your region", reply_markup=regions_btn)
    await message.answer(f"Please select your region", reply_markup=regions_inline_btn)
    await RegisterForm.region.set()
    # RegisterForm.first()


@dp.callback_query_handler(lambda call: call.data.startswith("region_select_"), state=RegisterForm.region)
async def select_region_handler(call, state: FSMContext):
    message = call.message
    region_id = call.data.split("_")[2]
    await state.update_data({"region_id": region_id})
    await RegisterForm.next()
    await message.delete()
    await message.answer(f"Select your city", reply_markup=get_cities_btn(region_id))


@dp.callback_query_handler(lambda call: call.data.startswith("select_city_"), state=RegisterForm.city)
async def select_city_handler(call, state: FSMContext):
    message = call.message
    city_id = call.data.split("_")[2]
    await state.update_data({"city_id": city_id})
    with connection.cursor() as cursor:
        cursor.execute("update users set city_id = %s where chat_id = %s", (city_id, message.chat.id))
        connection.commit()
    await message.answer(f"City id={city_id} selected")


@dp.callback_query_handler(lambda call: call.data.startswith("back_to_regions"))
async def back_to_regions_handler(call):
    message = call.message
    await message.delete()
    await message.answer(f"Please select your region", reply_markup=regions_inline_btn)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
        ]
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
