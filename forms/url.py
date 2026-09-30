from aiogram.fsm.state import State, StatesGroup


class UrlForm(StatesGroup):
    url = State()
