from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class RolePlayAdd(StatesGroup):
    cmd = State()
    text= State()
    textself = State()