from aiogram import F
from datetime import datetime
from bot import bot, states
from aiogram import Router, types, filters
from filters import RolePlayFilter
from models.chat import BanStick, RolePlay, User, Chat
from texts import roleplay as text

from fuzzywuzzy import fuzz
from utils import client
import re

from aiogram import Router
from midllwares import CounterMiddleware
router = Router()
router.message.middleware(CounterMiddleware())

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


@router.message(filters.Command('rp'))
async def getRules(message: types.Message):
    cmds = []
    rps = RolePlay.select()
    for rp in rps:
        cmds.append(rp.cmd)
    cmds_ = "\n".join(cmds)
    await message.answer(f'{text.RP}{cmds_}', parse_mode='html')

@router.message(F.text.startswith('*ущипнуть'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*ущипнуть')
    if mtxt == '':
        await message.answer(text.PINCH_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.PINCH.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*ударить'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*ударить')
    if mtxt == '':
        await message.answer(text.HIT_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.HIT.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*выебать'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*выебать')
    if mtxt == '':
        await message.answer(text.FUCK_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.FUCK.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*дать пять'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*дать пять')
    if mtxt == '':
        await message.answer(text.FIVE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.FIVE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*испугать'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*испугать')
    if mtxt == '':
        await message.answer(text.SCARE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.SCARE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*записать на ноготочки'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*записать на ноготочки')
    if mtxt == '':
        await message.answer(text.WRITE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.WRITE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*обнять'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*обнять')
    if mtxt == '':
        await message.answer(text.HUG_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.HUG.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*пригласить на чаек'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*пригласить на чаек')
    if mtxt == '':
        await message.answer(text.INVITE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.INVITE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*извиниться'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*извиниться')
    if mtxt == '':
        await message.answer(text.SORRY_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.SORRY.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*кусь'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*кусь')
    if mtxt == '':
        await message.answer(text.BITE_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.BITE.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*кастрировать'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*кастрировать')
    if mtxt == '':
        await message.answer(text.CAST_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.CAST.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*лизнуть'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Лизнуть')
    if mtxt == '':
        await message.answer(text.LICK_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.LICK.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*лизь'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Лизь')
    if mtxt == '':
        await message.answer(text.LICK_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.LICK.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*отравить'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Отравить')
    if mtxt == '':
        await message.answer(text.POISON_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.POISON.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*поздравить'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Поздравить')
    if mtxt == '':
        await message.answer(text.CONG_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.CONG.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*поцеловать'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*Поцеловать')
    if mtxt == '':
        await message.answer(text.KISS_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.KISS.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*уложить спать'))
async def role_play_handler(message: types.Message):
    mtxt= replace_(message.text, '*уложить спать')
    if mtxt == '':
        await message.answer(text.SLEEP_SELF.format(username=message.from_user.username))
        await message.delete()
    else:
        await message.answer(text.SLEEP.format(username=message.from_user.username, _username=mtxt))
        await message.delete()

@router.message(F.text.startswith('*посмотреть дракона'))
async def role_play_handler(message: types.Message):
    mtxt= mtxt = message.text[len('*посмотреть дракона'):]
    mtxt = mtxt.strip()
    if mtxt == '':
        await message.answer(text.SEE_DRAGON_SELF.format(username=message.from_user.username), parse_mode='html')
        await message.delete()
    else:
        await message.answer(text.SEE_DRAGON.format(username=message.from_user.username, _username=mtxt), parse_mode='html')
        await message.delete()

@router.message(F.text.startswith('*пойти гулять'))
async def role_play_handler(message: types.Message):
    mtxt= mtxt = message.text[len('*пойти гулять'):]
    mtxt = mtxt.strip()
    if mtxt == '':
        await message.answer(text.WALK_SELF.format(username=message.from_user.username), parse_mode='html')
        await message.delete()
    else:
        await message.answer(text.WALK.format(username=message.from_user.username, _username=mtxt), parse_mode='html')
        await message.delete()

@router.message(F.text.startswith('*кататься'))
async def role_play_handler(message: types.Message):
    mtxt= mtxt = message.text[len('*кататься'):]
    mtxt = mtxt.strip()
    if mtxt == '':
        await message.answer(text.RIDE_SELF.format(username=message.from_user.username), parse_mode='html')
        await message.delete()
        
    else:
        await message.answer(text.RIDE.format(username=message.from_user.username, _username=mtxt), parse_mode='html')
        await message.delete( )
