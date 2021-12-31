from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from keyboards.inline import get_chapter_inline_markup
from loader import dp


@dp.message_handler(CommandStart(), state='*')
async def _bot_start(message: Message, session, state):
    text = 'Выберите тему 👇'

    await state.finish()

    await message.answer(text, reply_markup=await get_chapter_inline_markup(session))
