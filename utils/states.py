from aiogram.fsm.state import StatesGroup, State

class PickState(StatesGroup):
    info_viewing = State()
    menu_viewing = State()
    commands_viewing = State()
    function_unavailable = State()
    tt_assistant = State()
    tt_downloading = State()
    tt_generating_tags = State()
    talking_chatgpt = State()
    checking_todo_menu = State()
    browsing_tasks = State()
    adding_new_task = State()
    anime_assistant = State()
    browsing_news = State()
    looking_for_sauce = State()
    sending_feedback = State()
    buying_coffee = State()