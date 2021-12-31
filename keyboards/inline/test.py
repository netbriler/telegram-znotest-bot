from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.questions import Question, count_questions
from services.tests import get_tests


async def get_test_inline_markup(session, chapter_id: int):
    markup = InlineKeyboardMarkup()

    for test in await get_tests(session, chapter_id):
        markup.add(InlineKeyboardButton(f'{test.name} ({await count_questions(session, test.id)})',
                                        callback_data=f'test_{test.id}'))

    markup.add(InlineKeyboardButton('🔙 Назад', callback_data=f'chapters'))
    return markup
