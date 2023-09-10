from aiogram import types
import random
from models.chat import User
from bot import bot
from aiogram_calendar import DialogCalendar 

async def checkBirthday(message: types.Message):
    user = User.get(User.tgid == message.from_user.id)
    if message.from_user.id != 285635206:
        if user.date_birthday == None and random.choices([True, False], [10,40])[0]:
            try:
                await bot.send_message(message.from_user.id,'Когда вы родились?', reply_markup=await DialogCalendar().start_calendar())
            except:
                await message.reply('Напишите сударь мне в личные сообщения❗️❕❗️ И напишите после этого здесь что-то ❗️❕❗️')
