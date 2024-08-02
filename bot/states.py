from aiogram.fsm.state import State, StatesGroup


class AddMessageSG(StatesGroup):
    username = State()
    text = State()
