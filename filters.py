from aiogram import types
from typing import Union

from aiogram.filters import BaseFilter
from models.chat import RolePlay
from bot import dp

class RolePlayFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message) -> bool:
        rps = RolePlay.select()
        for rp in rps:
            cmd = rp.cmd
            if message.text.startswith( cmd):
                return True
        return False
