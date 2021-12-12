from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.tests import get_tests


async def get_test_inline_markup(session, chapter_id: int):
    markup = InlineKeyboardMarkup()

    for test in await get_tests(session, chapter_id):
        markup.add(InlineKeyboardButton(test.name, callback_data=f'test_{test.id}'))

    markup.add(InlineKeyboardButton('🔙 Назад', callback_data=f'chapters'))
    return markup


def get_test_question_inline_markup(question_id: int):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('❓ Решение', callback_data=f'question_{question_id}_solution'))
    markup.add(InlineKeyboardButton('➡ Следующее', callback_data=f'question_{question_id}_next'))

    markup.add(InlineKeyboardButton('🔙 Назад', callback_data=f'chapters'))
    return markup
