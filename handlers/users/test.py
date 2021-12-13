import random

from aiogram.types import CallbackQuery

from keyboards.inline import get_test_question_inline_markup
from loader import dp
from services.questions import get_questions, get_question
from services.tests import get_test
from states import States
from utils.helper import clean_messages


@dp.callback_query_handler(text='chapters', state='*')
async def _back_to_chapters(callback_query: CallbackQuery, session):
    await callback_query.message.edit_reply_markup(reply_markup=await get_chapter_inline_markup(session))


@dp.callback_query_handler(is_test=True, state='*')
async def _select_test(callback_query: CallbackQuery, session, test, state):
    message_to_delete = await _send_question(callback_query, session, test.id, state)

    await callback_query.message.delete()

    await States.test.set()

    async with state.proxy() as data:
        data['delete_messages'] = [message_to_delete.message_id]


@dp.callback_query_handler(is_question=True, state=States.test)
async def _question(callback_query: CallbackQuery, session, question, action, state):
    if action == 'next':
        await clean_messages(state, callback_query.message)

        message_to_delete = await _send_question(callback_query, session, question.test_id, state)
    elif action == 'solution':
        if question.explanation_image:
            message_to_delete = await callback_query.message.answer_photo(
                f'https://zno.osvita.ua{question.explanation_image}',
                caption=question.explanation)
        else:
            message_to_delete = await callback_query.message.answer(question.explanation)
    else:
        return await callback_query.answer('Такая команда не найдена. Попробуйте снова', show_alert=True)

    async with state.proxy() as data:
        if 'delete_messages' not in data:
            data['delete_messages'] = list()

        data['delete_messages'].append(message_to_delete.message_id)

    await callback_query.answer('👍')


@dp.callback_query_handler(state=States.test, is_answer=True)
async def _answer(callback_query: CallbackQuery, match, state, session):
    wrong_answer = None

    if match == 'label':
        return await callback_query.answer('Выберите ответ ⬜')
    elif match == 'submit':
        async with state.proxy() as data:
            if 'selected_answer' not in data:
                return await callback_query.answer('Для начала выберите ответ ⬜')

            id = data['selected_answer']

            question = await get_question(session, data['question_id'])

        if id == int(question.answer_test):
            await callback_query.answer('Верно ✅')

            await clean_messages(state, callback_query.message)

            if 'delete_messages' not in data:
                data['delete_messages'] = list()

            message_to_delete = await _send_question(callback_query, session, question.test_id, state)

            async with state.proxy() as data:
                data['delete_messages'].append(message_to_delete.message_id)

            return
        await callback_query.answer('Не верно ❌')

        wrong_answer = id
        id = int(question.answer_test)
    else:
        async with state.proxy() as data:
            id = int(match)
            data['selected_answer'] = id
            await callback_query.answer('Выбрано 👍')

    await callback_query.message.edit_reply_markup(
        reply_markup=get_test_question_inline_markup(await get_question(session, data['question_id']),
                                                     data['chapter_id'], id, wrong_answer))


async def _send_question(callback_query: CallbackQuery, session, test_id, state):
    question = random.choice(await get_questions(session, test_id))

    test = await get_test(session, test_id)

    async with state.proxy() as data:
        data['question_id'] = question.id
        data['test_id'] = test.id
        data['chapter_id'] = test.chapter_id
        if 'selected_answer' in data:
            del data['selected_answer']

    if question.question_image:
        return await callback_query.message.answer_photo(f'https://zno.osvita.ua{question.question_image}',
                                                         caption=question.question,
                                                         reply_markup=get_test_question_inline_markup(question,
                                                                                                      test.chapter_id))
    return await callback_query.message.answer(question.question,
                                               reply_markup=get_test_question_inline_markup(question,
                                                                                            test.chapter_id))
