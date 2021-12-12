from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.inline import get_test_inline_markup, get_chapter_inline_markup
from loader import dp


@dp.message_handler(CommandStart())
async def _select_test(message: Message, session):
    text = 'Выбери раздел'

    await message.answer(text, reply_markup=await get_test_inline_markup(session))


@dp.callback_query_handler(text='chapters', state='*')
async def _back_to_chapters(callback_query: CallbackQuery, session):
    await callback_query.message.edit_reply_markup(reply_markup=await get_chapter_inline_markup(session))


@dp.callback_query_handler(is_chapter=True)
async def _select_chapter(callback_query: CallbackQuery, session, chapter):
    await callback_query.message.edit_reply_markup(reply_markup=await get_test_inline_markup(session, chapter.id))
