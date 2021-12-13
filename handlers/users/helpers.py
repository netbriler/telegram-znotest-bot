from aiogram.types import Message, CallbackQuery

from keyboards.inline import get_chapter_inline_markup
from loader import dp
from utils.helper import clean_messages


@dp.message_handler(state='*')
async def _default(message: Message, session, state):
    text = 'Выберите тему 👇'

    await state.finish()

    await message.answer(text, reply_markup=await get_chapter_inline_markup(session))


@dp.callback_query_handler(state='*')
async def _default_inline(callback_query: CallbackQuery, session, state):
    await clean_messages(state, callback_query.message)
    await callback_query.message.delete()

    text = 'Выберите тему 👇'

    await callback_query.message.answer(text, reply_markup=await get_chapter_inline_markup(session))

    await state.finish()

    await callback_query.answer('Такая команда не найдена. Попробуйте снова', show_alert=True)
