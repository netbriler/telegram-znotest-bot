from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.questions import Question


def get_question4x1_inline_markup(question: Question, chapter_id: int, selected_answer=None, wrong_answer=None,
                                  is_answered=False):
    markup = InlineKeyboardMarkup(row_width=5)

    markup.add(*[InlineKeyboardButton(_, callback_data=f'question_{question.id}_label') for _ in
                 ['А', 'Б', 'В', 'Г', 'Д']])

    for i in range(1, 6):
        markup.insert(InlineKeyboardButton('✅' if i == selected_answer else '❌' if i == wrong_answer else '⬜',
                                           callback_data=f'answer_{i}'))

    return _get_base_question_inline_markup(markup, question, chapter_id, is_answered)


def get_question4x4_inline_markup(question: Question, chapter_id: int,
                                  selected_answers=None, wrong_answers=None, is_answered=False):
    if wrong_answers is None:
        wrong_answers = [None, None, None, None]
    if selected_answers is None:
        selected_answers = [None, None, None, None]

    markup = InlineKeyboardMarkup(row_width=6)

    markup.add(*[InlineKeyboardButton(_, callback_data=f'question_{question.id}_label') for _ in
                 ['⠀', 'А', 'Б', 'В', 'Г', 'Д']])

    for i in range(1, 5):
        markup.insert(InlineKeyboardButton(i, callback_data=f'question_{question.id}_label'))
        for j in range(1, 6):
            markup.insert(
                InlineKeyboardButton('✅' if j == selected_answers[i - 1] else '❌' if j == wrong_answers[i - 1] else '⬜',
                                     callback_data=f'answer_{i}_{j}'))

    return _get_base_question_inline_markup(markup, question, chapter_id, is_answered)


def _get_base_question_inline_markup(markup: InlineKeyboardMarkup, question: Question, chapter_id: int,
                                    is_answered=False):
    if not is_answered:
        markup.insert(InlineKeyboardButton('🚩 Ответить', callback_data='answer_submit'))

    markup.add(InlineKeyboardButton('❓ Решение', callback_data=f'question_{question.id}_solution'),
               InlineKeyboardButton('➡ Следующее', callback_data=f'question_{question.id}_next'))

    markup.add(InlineKeyboardButton('🔙 Назад', callback_data=f'chapter_{chapter_id}'))
    return markup
