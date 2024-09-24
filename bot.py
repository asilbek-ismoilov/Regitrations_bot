import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import Registor

TOKEN = "BOT_TOKEN"

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    full_name = message.from_user.full_name
    text = f"Salom {full_name}, Ro'yxatdan o'tish botga hush kelibsiz"
    await message.answer(text)

@dp.message(Command("reg"))
async def register(message: Message, state:FSMContext):
    await message.answer("Ro'yxatdan o'tish uchun ma'limotlarni kiriting !  \nIsmingizni kiriting ")
    await state.set_state(Registor.ism)

@dp.message(F.text, Registor.ism)
async def register_ism(message: Message, state:FSMContext):
    ism = message.text   # Temur
    # {"name": "Temur"}
    await state.update_data(name = ism)
    await state.set_state(Registor.familiya)
    await message.answer("Familiyani kiriting")

@dp.message(F.text, Registor.familiya)
async def register_familiya(message: Message, state:FSMContext):
    familiya = message.text  # Valiyev
    # {"name": "Temur", "surname" : "Valiyev"}
    await state.update_data(surname = familiya)
    await state.set_state(Registor.yosh)
    await message.answer("Yoshingizni kiriting")

@dp.message(F.text, Registor.yosh)
async def register_yosh(message: Message, state:FSMContext):
    yosh = message.text  # "12"
    # {"name": "Temur", "surname" : "Valiyev", "age": "12"}
    await state.update_data(age = yosh)
    await state.set_state(Registor.tel)
    await message.answer("Telefon raqamni kiriting")

@dp.message(F.text, Registor.tel)
async def register_tel(message: Message, state:FSMContext):
    tel = message.text   # +998974020330
    # {"name": "Temur", "surname" : "Valiyev", "age": "12", "tel": "+998974020330"}
    await state.update_data(tel = tel)
    await state.set_state(Registor.kurs)
    await message.answer("Kursni nomini kiriting")

@dp.message(F.text, Registor.kurs)
async def register_kurs(message: Message, state:FSMContext):

    # baza = {"name": "Temur", "surname" : "Valiyev", "age": "12", "tel": "+998974020330"}
    
    data = await state.get_data() # Ma'lumotlarni (ba'zadan) olish

    # ba'zadan ma'lumotlarni olish
    ism = data.get("name")
    familiya = data.get("surname")
    yosh = data.get("age")
    tel = data.get("tel")
    
    kurs = message.text  # Python

    text = f"Ism : {ism} \nFamiliya : {familiya} \nYosh : {yosh} \nTel : {tel} \nKurs : {kurs}"
    await message.answer("Siz ro'yxatdan o'tdingiz")
    await bot.send_message(chat_id= ADIM_ID, text=text)
    await state.clear()
    
async def main():
    global bot
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
