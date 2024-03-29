from keyboards import inline
from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from utils import text, secret_values, parser
from utils.states import PickState
from database.db import Database as db

router = Router()
dp = Dispatcher()
bot = Bot(token=secret_values.TOKEN, parse_mode='HTML')

@router.callback_query(F.data=='tiktok')
async def cb_tiktok(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(PickState.tt_assistant)
    await cb.message.answer(text.tt_assistant_menu, reply_markup=inline.tiktok_assistant_kb)

@router.callback_query(F.data=='download_video')
async def cb_download_video(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(PickState.tt_downloading)
    await cb.message.answer(text.tt_video_download)

@router.callback_query(F.data=='generate_tags')
async def cb_generate_tags(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(PickState.tt_generating_tags)
    await cb.message.answer(text.tt_generate_tags)

@router.callback_query(F.data=='chatgpt')
async def cb_chatgpt(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(PickState.talking_chatgpt)
    await cb.message.answer(text.talk_chatgpt)

@router.callback_query(F.data=='todo')
async def cb_todo(cb: CallbackQuery, state: FSMContext, db: db):
    await cb.answer()
    await state.set_state(PickState.checking_todo_menu)
    await cb.message.answer(text.todo_info, reply_markup=inline.todo_kb)
    db.delete_old_tasks()

@router.callback_query(F.data=='add_task')
async def cb_add_task(cb: CallbackQuery, state: FSMContext, db: db):
    await cb.answer()
    await state.set_state(PickState.adding_new_task)
    await cb.message.answer(text.add_task)
    db.delete_old_tasks()

@router.callback_query(F.data=='my_tasks')
async def cb_my_tasks(cb: CallbackQuery, state: FSMContext, db: db):
    await cb.answer()
    await state.set_state(PickState.browsing_tasks)
    db.delete_old_tasks()
    await cb.message.answer(db.get_formated_tasks(cb.from_user.id))

@router.callback_query(F.data=='anime')
async def cb_anime(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(PickState.anime_assistant)
    await cb.message.answer(text.anime_assistant_menu, reply_markup=inline.anime_assistant_kb)

@router.callback_query(F.data=='anime_news')
async def cb_browse_news(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(PickState.browsing_news)
    proc = await cb.message.answer(text.processing_info)
    news = await parser.get_news()
    await cb.message.answer(news)
    await proc.delete()

@router.callback_query(F.data=='sauce')
async def cb_find_sauce(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(PickState.looking_for_sauce)
    await cb.message.answer(text.find_sauce)

@router.callback_query(F.data=='feedback')
async def cb_send_feedback(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(PickState.sending_feedback)
    await cb.message.answer(text.send_feedback)

@router.callback_query(F.data=='buy_coffee')
async def cb_buy_coffee(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(PickState.buying_coffee)
    await cb.message.answer(text.buy_coffee)