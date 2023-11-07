import random
from aiogram import types
from models.chat import User
from bot import bot, states

async def checkBirthday(message: types.Message):
    pass
    # if message.from_user.id != 285635206:
    #     user = User.get((User.tgid == message.from_user.id) & (User.chat == message.chat.id))
    #     if user.date_birthday == None and random.choices([True, False], [10,40])[0]:
    #         if user.date_birthday == None:
    #             states[str(message.from_user.id)] = message.chat.id 
    #             try:
    #                 await bot.send_message(message.from_user.id,'Когда вы родились?', reply_markup=await DialogCalendar().start_calendar())
    #             except:
    #                 await message.reply('Напишите, [сударь\сударыня], мне в личные сообщения❗️❕❗️ И напишите после этого здесь что-то ❗️❕❗️')