from datetime import datetime
from bot import dp, states
from aiogram import types, filters
from filters import RolePlayFilter
from models.chat import BanStick, RolePlay, User, Chat
from texts import roleplay as text

from fuzzywuzzy import fuzz
from aiogram_calendar import dialog_cal_callback, DialogCalendar
from utils import client
import re

def replace_(text, old_word):
    """
    Заменяет слово в тексте с учетом всех возможных комбинаций регистров.

    Параметры:
        text (str): Исходный текст.
        old_word (str): Слово, которое нужно заменить.
        new_word (str): Новое слово для замены.

    Возвращает:
        str: Текст с заменой всех вхождений old_word на new_word с учетом всех комбинаций регистров.
    """
    variations = []
    n = len(old_word)

    # Генерируем все возможные комбинации регистров для слова old_word
    for i in range(2 ** n):
        variation = ""
        for j in range(n):
            variation += old_word[j].lower() if i & (1 << j) else old_word[j].upper()
        variations.append(variation)

    # Заменяем слова с учетом различных регистров
    for var in variations:
        text = text.replace(var, '')

    return text


@dp.message_handler(commands=['rp'])
async def getRules(message: types.Message):
    cmds = []
    rps = RolePlay.select()
    for rp in rps:
        cmds.append(rp.cmd)
    cmds_ = "\n".join(cmds)
    await message.answer(f'{text.RP}{cmds_}', parse_mode='html')

@dp.message_handler(lambda message: message.text.lower().startswith('*ущипнуть'))
async def role_play_handler(message: types.Message):
    # mtxt = message.text.replace("*ущипнуть", '').replace("*УЩИПНУТЬ", '').replace("*ущипнуть ", '').replace("*УЩИПНУТЬ ", '')
    mtxt= replace_(message.text, '*ущипнуть')
    # mtxt = remove_w(message.text, '*ущипнуть')
    if mtxt == '':
        await message.answer(text.PINCH_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.PINCH.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*ударить'))
async def role_play_handler(message: types.Message):
    #mtxt = message.text.replace("*ударить", '').replace("*УДАРИТЬ", '').replace("*ударить ", '').replace("*УДАРИТЬ ", '')
    mtxt= replace_(message.text, '*ударить')
    # mtxt = remove_w(message.text, '*ущипнуть')
    if mtxt == '':
        await message.answer(text.HIT_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.HIT.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*выебать'))
async def role_play_handler(message: types.Message):
   # mtxt = message.text.replace("*выебать", '').replace("*ВЫЕБАТЬ", '').replace("*выебать ", '').replace("*ВЫЕБАТЬ ", '')
    mtxt= replace_(message.text, '*выебать')
    if mtxt == '':
        await message.answer(text.FUCK_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.FUCK.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*дать пять'))
async def role_play_handler(message: types.Message):
    #mtxt = message.text.replace("*дать пять", '').replace("*дать пять ", '').replace("*ДАТЬ ПЯТЬ", '').replace("*ДАТЬ ПЯТЬ ", '')
    mtxt= replace_(message.text, '*дать пять')
    if mtxt == '':
        await message.answer(text.FIVE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.FIVE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*испугать'))
async def role_play_handler(message: types.Message):
    #mtxt = message.text.replace("*испугать", '').replace("*ИСПУГАТЬ", '')
    mtxt= replace_(message.text, '*испугать')
    if mtxt == '':
        await message.answer(text.SCARE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.SCARE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*записать на ноготочки'))
async def role_play_handler(message: types.Message):
    #mtxt = message.text.replace("*записать на ноготочки", '').replace("*записать на ноготочки ", '').replace("*ЗАПИСАТЬ НА НОГОТОЧКИ", '').replace('*ЗАПИСАТЬ НА НОГОТОЧКИ ', '')
    mtxt= replace_(message.text, '*записать на ноготочки')
    if mtxt == '':
        await message.answer(text.WRITE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.WRITE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*обнять'))
async def role_play_handler(message: types.Message):
    #mtxt = message.text.replace("*обнять", '').replace("*ОБНЯТЬ", '').replace('*обнять ', '').replace('*ОБНЯТЬ ', '')
    mtxt= replace_(message.text, '*обнять')
    if mtxt == '':
        await message.answer(text.HUG_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.HUG.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*пригласить на чаек'))
async def role_play_handler(message: types.Message):
    # mtxt = message.text.replace("*пригласить на чаек", '').replace("*ПРИГЛАСИТЬ НА ЧАЕК", '').replace('*ПРИГЛАСИТЬ НА ЧАЕК ', '').replace('*пригласить на чаек ', '')
    mtxt= replace_(message.text, '*пригласить на чаек')
    if mtxt == '':
        await message.answer(text.INVITE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.INVITE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*извиниться'))
async def role_play_handler(message: types.Message):
    # mtxt = message.text.replace("*Извиниться", '').replace("*ИЗВИНИТЬСЯ", '').replace('*извиниться ', '').replace('*ИЗВИНИТЬСЯ ', '')
    mtxt= replace_(message.text, '*извиниться')
    if mtxt == '':
        await message.answer(text.SORRY_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.SORRY.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*кусь'))
async def role_play_handler(message: types.Message):
    # mtxt = message.text.replace("*кусь", '').replace("*КУСЬ", '').replace('*кусь ', '').replace('*КУСЬ ', '')
    mtxt= replace_(message.text, '*кусь')
    if mtxt == '':
        await message.answer(text.BITE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.BITE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*кастрировать'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*кастрировать')
    if mtxt == '':
        await message.answer(text.CAST_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.CAST.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*лизнуть'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Лизнуть')
    if mtxt == '':
        await message.answer(text.LICK_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.LICK.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*лизь'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Лизь')
    if mtxt == '':
        await message.answer(text.LICK_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.LICK.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*отравить'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Отравить')
    if mtxt == '':
        await message.answer(text.POISON_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.POISON.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*поздравить'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Поздравить')
    if mtxt == '':
        await message.answer(text.CONG_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.CONG.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*поцеловать'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Поцеловать')
    if mtxt == '':
        await message.answer(text.KISS_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.KISS.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*уложить спать'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*уложить спать')
    if mtxt == '':
        await message.answer(text.SLEEP_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.SLEEP.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*посмотреть дракона'))
async def role_play_handler(message: types.Message):
    mtxt= mtxt = message.text[len('*посмотреть дракона'):]
    mtxt = mtxt.strip()
    if mtxt == '':
        await message.answer(text.SEE_DRAGON_SELF.format(username=message.from_user.username), parse_mode='html')
        await message.delete()
    else:
        await message.answer(text.SEE_DRAGON.format(username=message.from_user.username, _username=mtxt), parse_mode='html')
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*пойти гулять'))
async def role_play_handler(message: types.Message):
    mtxt= mtxt = message.text[len('*пойти гулять'):]
    mtxt = mtxt.strip()
    if mtxt == '':
        await message.answer(text.WALK_SELF.format(username=message.from_user.username), parse_mode='html')
        await message.delete()
    else:
        await message.answer(text.WALK.format(username=message.from_user.username, _username=mtxt), parse_mode='html')
        await message.delete()

@dp.message_handler(lambda message: message.text.lower().startswith('*кататься'))
async def role_play_handler(message: types.Message):
    mtxt= mtxt = message.text[len('*кататься'):]
    mtxt = mtxt.strip()
    if mtxt == '':
        await message.answer(text.RIDE_SELF.format(username=message.from_user.username), parse_mode='html')
        await message.delete()
    else:
        await message.answer(text.RIDE.format(username=message.from_user.username, _username=mtxt), parse_mode='html')
        await message.delete()
