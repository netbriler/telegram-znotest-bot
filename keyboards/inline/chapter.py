from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.chapters import get_chapters


async def get_chapter_inline_markup(session):
    markup = InlineKeyboardMarkup()

    for chapter in await get_chapters(session):
        markup.add(InlineKeyboardButton(chapter.name, callback_data=f'chapter_{chapter.id}'))

    return markup
