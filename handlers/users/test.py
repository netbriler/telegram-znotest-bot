import random

from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.inline import get_test_inline_markup, get_test_question_inline_markup
from loader import dp
from services.questions import get_questions


@dp.message_handler(CommandStart())
async def _select_test(message: Message, session):
    text = 'Выбери раздел'

    await message.answer(text, reply_markup=await get_test_inline_markup(session))


@dp.callback_query_handler(text='chapters', state='*')
async def _back_to_chapters(callback_query: CallbackQuery, session):
    await callback_query.message.edit_reply_markup(reply_markup=await get_chapter_inline_markup(session))


@dp.callback_query_handler(is_test=True)
async def _select_test(callback_query: CallbackQuery, session, test):
    await _send_question(callback_query, session, test.id)


@dp.callback_query_handler(is_question=True)
async def _question(callback_query: CallbackQuery, session, question, action):
    if action == 'next':
        await _send_question(callback_query, session, question.test_id)
    elif action == 'solution':
        if question.explanation_image:
            await callback_query.message.answer_photo(f'https://zno.osvita.ua{question.explanation_image}',
                                                      caption=question.explanation)
        else:
            await callback_query.message.answer(question.explanation)


async def _send_question(callback_query: CallbackQuery, session, test_id):
    question = random.choice(await get_questions(session, test_id))

    if question.question_image:
        await callback_query.message.answer_photo(f'https://zno.osvita.ua{question.question_image}',
                                                  caption=question.question,
                                                  reply_markup=get_test_question_inline_markup(question.id))
    else:
        await callback_query.message.answer(question.question,
                                            reply_markup=get_test_question_inline_markup(question.id))

    # await callback_query.message.delete()
