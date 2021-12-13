from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.questions import Question
from services.tests import get_tests


async def get_test_inline_markup(session, chapter_id: int):
    markup = InlineKeyboardMarkup()

    for test in await get_tests(session, chapter_id):
        markup.add(InlineKeyboardButton(test.name, callback_data=f'test_{test.id}'))

    markup.add(InlineKeyboardButton('🔙 Назад', callback_data=f'chapters'))
    return markup


def get_test_question_inline_markup(question: Question, chapter_id: int, selected_answer=None, wrong_answer=None):
    markup = InlineKeyboardMarkup(row_width=5)

    if question.test_type == '4x1':
        markup.add(*[InlineKeyboardButton(_, callback_data=f'answer_label') for _ in ['А', 'Б', 'В', 'Г', 'Д']])

        for i in range(1, 6):
            markup.insert(InlineKeyboardButton('✅' if i == selected_answer else '❌' if i == wrong_answer else '⬜',
                                               callback_data=f'answer_{i}'))

        markup.insert(InlineKeyboardButton('🚩 Ответить', callback_data='answer_submit'))

    markup.add(InlineKeyboardButton('❓ Решение', callback_data=f'question_{question.id}_solution'),
               InlineKeyboardButton('➡ Следующее', callback_data=f'question_{question.id}_next'))

    markup.add(InlineKeyboardButton('🔙 Назад', callback_data=f'chapter_{chapter_id}'))
    return markup
