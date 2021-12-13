from aiogram.types import CallbackQuery

from keyboards.inline import get_test_inline_markup, get_chapter_inline_markup
from loader import dp


@dp.callback_query_handler(text='chapters', state='*')
async def _back_to_chapters(callback_query: CallbackQuery, session):
    await callback_query.message.delete()

    await callback_query.message.answer('Выберите тему 👇', reply_markup=await get_chapter_inline_markup(session))


@dp.callback_query_handler(is_chapter=True, state='*')
async def _select_chapter(callback_query: CallbackQuery, session, chapter):
    await callback_query.message.delete()

    await callback_query.message.answer('Выберите тест 👇', reply_markup=await get_test_inline_markup(session, chapter.id))
