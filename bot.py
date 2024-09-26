import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import Registor

TOKEN = "7015438221:AAGQYE-XxJwfNnOr_2fxGPctceAPLvhHDYQ"
ADMIN_ID = [5012784380, 6324104324, 7241341727, 6598593846]

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

# First_name
@dp.message(F.text, Registor.ism)
async def register_ism(message: Message, state:FSMContext):
    photo = message.text
    await state.update_data(rasm = photo)
    await state.set_state(Registor.familiya)
    await message.answer("Familiyani kiriting")

# Agar kiritilgan qiymat text bo'lmasa ushbu kod ishga tushadi
@dp.message(Registor.ism)
async def register_ism_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Ismimgizni to'g'ri kiriting ❗️")

# end First_name

@dp.message(F.text, Registor.familiya)
async def register_familiya(message: Message, state:FSMContext):
    familiya = message.text 
    await state.update_data(surname = familiya)
    await state.set_state(Registor.yosh)
    await message.answer("Yoshingizni kiriting")

@dp.message(F.text, Registor.yosh)
async def register_yosh(message: Message, state:FSMContext):
    yosh = message.text
    await state.update_data(age = yosh)
    await state.set_state(Registor.tel)
    await message.answer("Telefon raqamni kiriting")

# Phone_number
@dp.message(F.text.regexp(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"), Registor.tel)
async def register_tel(message: Message, state:FSMContext):
    tel = message.text
    await state.update_data(tel = tel)
    await state.set_state(Registor.kurs)
    await message.answer("Kursni nomini kiriting")

@dp.message(Registor.tel)
async def register_tel_del(message:Message, state:FSMContext):
    await message.delete()
    await message.answer(text= "Telefon raqamni to'g'ri kiriting ❗️")

# end Phone_number

@dp.message(F.text, Registor.kurs)
async def register_kurs(message: Message, state:FSMContext):

    data = await state.get_data() 

    ism = data.get("name")
    familiya = data.get("surname")
    yosh = data.get("age")
    tel = data.get("tel")
    
    kurs = message.text

    text = f"Ism : {ism} \nFamiliya : {familiya} \nYosh : {yosh} \nTel : {tel} \nKurs : {kurs}"
    await message.answer("Siz ro'yxatdan o'tdingiz")

    for admin in ADMIN_ID:
        await bot.send_message(chat_id= admin, text=text)
    await state.clear()

@dp.startup()
async def bot_start():
    for admin in ADMIN_ID:
        await bot.send_message(admin, "Tabriklaymiz 🎉 \nBotimiz ishga tushdi ")

@dp.shutdown()
async def bot_start():
    for admin in ADMIN_ID:
        await bot.send_message(admin, "Bot to'xtadi ❗️")

    
async def main():
    global bot
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
