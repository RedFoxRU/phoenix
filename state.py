from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class RolePlayAdd(StatesGroup):
    cmd = State()
    text= State()
    textself = State()