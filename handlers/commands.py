import asyncio

from aiogram import Router
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext 
from datetime import datetime
from keyboards import inline
from utils import text, secret_values, parser
from utils.states import PickState
from database.db import Database as db

router = Router()

@router.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext, db: db):
    if not db.user_exists(msg.from_user.id):
        formated_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
        db.add_user(user_id= msg.from_user.id, user_name= msg.from_user.username, first_launch= formated_datetime)
    await state.set_state(PickState.info_viewing)
    await msg.answer(text.greeting.format(name=msg.from_user.full_name.title()), reply_markup=inline.main_kb)

@router.message(Command('info'))
async def cmd_info(msg: Message, state: FSMContext):
    await state.set_state(PickState.info_viewing)
    await msg.answer(text.info)

@router.message(Command('menu'))
async def cmd_menu(msg: Message, state: FSMContext):
    await state.set_state(PickState.menu_viewing)
    await msg.answer(text.menu, reply_markup=inline.main_kb)

@router.message(Command('commands'))
async def cmd_commands(msg: Message, state: FSMContext):
    await state.set_state(PickState.commands_viewing)
    await msg.answer(text.see_commands)

@router.message(Command('video'))
async def cmd_video(msg: Message, state: FSMContext):
    await state.set_state(PickState.tt_downloading)
    await msg.answer(text.tt_video_download)

@router.message(Command('hashtags'))
async def cmd_hashtags(msg: Message, state: FSMContext):
    await state.set_state(PickState.tt_generating_tags)
    await msg.answer(text.tt_generate_tags)

@router.message(Command('chatgpt'))
async def cmd_chatgpt(msg: Message, state: FSMContext):
    await state.set_state(PickState.talking_chatgpt)
    await msg.answer(text.talk_chatgpt)

@router.message(Command('todo'))
async def cmd_todo(msg: Message, state: FSMContext, db: db):
    await state.set_state(PickState.checking_todo_menu)
    await msg.answer(text.todo_info, reply_markup=inline.todo_kb)
    db.delete_old_tasks()

@router.message(Command('newtask'))
async def cmd_newtask(msg: Message, state: FSMContext, db: db):
    await state.set_state(PickState.adding_new_task)
    db.delete_old_tasks()
    try:
        task_info = msg.text.replace("/newtask", "").strip()
        task_data = task_info.split('#')

        if len(task_data) >= 2:
            task_description = task_data[0].strip()
            task_datetime_str = task_data[1].strip()
            task_datetime = datetime.strptime(task_datetime_str, "%Y-%m-%d %H:%M")
            user_id = msg.from_user.id

            db.add_task(user_id, task_description, task_datetime)

            await msg.reply(text.adding_task_success.format(task=task_description, time= task_datetime))
            time_difference = task_datetime - datetime.now()

            await asyncio.sleep(time_difference.total_seconds())
            await msg.answer(text.task_remind.format(task= task_description, time= task_datetime))

        else:
            await msg.reply(text.adding_task_error)
            
    except Exception:
        await msg.reply(text.adding_task_error)

@router.message(Command('mytasks'))
async def cmd_mytasks(msg: Message, state: FSMContext, db: db):
    await state.set_state(PickState.browsing_tasks)
    db.delete_old_tasks()
    await msg.answer(db.get_formated_tasks(msg.from_user.id))

@router.message(Command('news'))
async def cmd_animenews(msg: Message, state: FSMContext):
    await state.set_state(PickState.browsing_news)
    proc = await msg.answer(text.processing_info)
    news = await parser.get_news()
    await msg.answer(news)
    await proc.delete()

@router.message(Command('sauce'))
async def cmd_sauce(msg: Message, state: FSMContext):
    await state.set_state(PickState.looking_for_sauce)
    await msg.answer(text.find_sauce)

@router.message(Command('feedback'))
async def cmd_feedback(msg: Message, state: FSMContext):
    await state.set_state(PickState.sending_feedback)
    await msg.answer(text.send_feedback)

@router.message(Command('coffee'))
async def cmd_coffee(msg: Message, state: FSMContext):
    await state.set_state(PickState.buying_coffee)
    await msg.answer(text.buy_coffee)