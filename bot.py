from aiogram import Dispatcher, Bot, types
from config import TOKEN
from loguru import logger
logger.add("test.log", level="INFO", format="{time} - {message}")

from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
states = {}


async def set_commands():
    await dp.bot.set_my_commands([
        types.BotCommand(command="/rule", description="Правила чата"),
        types.BotCommand(command="/inactive", description="Топ инактивов"),
        types.BotCommand(command="/actived", description="Топ активов"),
        types.BotCommand(command="/rp", description="РП команды"),
        types.BotCommand(command="/gprofile", description="Профиль группы (админ команда)"),
        types.BotCommand(command="/ban_stick", description="Забанить стикер (админ команда)"),
        types.BotCommand(command="/db", description="Данные о участниках чата (админ команда)"),
        types.BotCommand(command="/warn", description="Выдать предупреждение (админ команда)"),
        types.BotCommand(command="/warns", description="Просмотреть все предупреждения (админ команда)")
    ])
