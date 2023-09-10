from aiogram import types
from aiogram.dispatcher.filters import Filter
from models.chat import RolePlay
from bot import dp

class RolePlayFilter(Filter):
    key = "roleplayfilter"

    async def check(self, message: types.Message):
        _rp = []
        rps = RolePlay.select()
        for rp in rps:
            cmd = rp.cmd
            if cmd in message.text:
                _rp.append(rp.cmd)
                _rp.append(rp.textself)
                _rp.append(rp.text)
        if len (_rp) != 0:
            state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
            mtxt = message.text[len(_rp[0]):]
            mtxt = mtxt.strip()
            if mtxt == '':
                await message.answer(_rp[1].format(username=f'@{message.from_user.username}'), parse_mode='html')
                await message.delete()
            else:
                await message.answer(_rp[2].format(username=f'@{message.from_user.username}', _username=mtxt), parse_mode='html')
                await message.delete()
        return False
