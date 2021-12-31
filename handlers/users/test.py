import random

from aiogram.types import CallbackQuery

from keyboards.inline import get_question4x4_inline_markup, get_question4x1_inline_markup, get_chapter_inline_markup
from loader import dp
from services.questions import get_questions, get_question, count_questions
from services.tests import get_test
from states import Test
from utils.helper import clean_messages


@dp.callback_query_handler(is_test=True, state='*')
async def _select_test(callback_query: CallbackQuery, session, test, state):
    message_to_delete = await _send_question(callback_query, session, test.id, state)

    await callback_query.message.delete()

    async with state.proxy() as data:
        data['delete_messages'] = [message_to_delete.message_id]


@dp.callback_query_handler(is_question=True, state=[Test.question_4x1, Test.question_4x4])
async def _question(callback_query: CallbackQuery, session, question, action, state):
    if action == 'label':
        return await callback_query.answer('Выберите ответ ⬜')

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


@dp.callback_query_handler(state=Test.question_4x1, is_answer=True)
async def _answer_4x1(callback_query: CallbackQuery, match, state, session):
    async with state.proxy() as data:
        if data['is_answered']:
            return await callback_query.answer('Вы уже ответили, смотрите следующий вопрос ➡', show_alert=True)

    wrong_answer = None
    is_answered = False
    if match == 'submit':
        async with state.proxy() as data:
            if not data['selected_answer']:
                return await callback_query.answer('Для начала выберите ответ ⬜')

            selected_answer = data['selected_answer']
            question = await get_question(session, data['question_id'])

            if selected_answer == int(question.answer_test):
                data['user_balls'] += 1

        if selected_answer == int(question.answer_test):
            await callback_query.answer('Верно ✅')

            await clean_messages(state, callback_query.message)

            message_to_delete = await _send_question(callback_query, session, question.test_id, state)

            async with state.proxy() as data:
                data['delete_messages'] = [message_to_delete.message_id]

            return

        await callback_query.answer('Не верно ❌')

        wrong_answer = selected_answer
        selected_answer = int(question.answer_test)

        is_answered = True
        async with state.proxy() as data:
            data['is_answered'] = is_answered
    else:
        async with state.proxy() as data:
            data['selected_answer'] = match
            selected_answer = data['selected_answer']
            await callback_query.answer('Выбрано 👍')

    await callback_query.message.edit_reply_markup(
        reply_markup=get_question4x1_inline_markup(await get_question(session, data['question_id']),
                                                   data['chapter_id'], selected_answer=selected_answer,
                                                   wrong_answer=wrong_answer, is_answered=is_answered))


@dp.callback_query_handler(state=Test.question_4x4, is_answer=True)
async def _answer_4x4(callback_query: CallbackQuery, state, session, match, index):
    async with state.proxy() as data:
        if data['is_answered']:
            return await callback_query.answer('Вы уже ответили, смотрите следующий вопрос ➡', show_alert=True)

    wrong_answers = [None, None, None, None]
    is_answered = False
    if match == 'submit':
        async with state.proxy() as data:
            if None in data['selected_answers']:
                return await callback_query.answer('Для начала выберите ответы ⬜')

            question = await get_question(session, data['question_id'])

            right_answers = [int(_) for _ in question.answer_test.split(',')]

            for i in range(4):
                if data['selected_answers'][i] == right_answers[i]:
                    data['user_balls'] += 1

        if ','.join(str(_) for _ in data['selected_answers']) == question.answer_test:
            await callback_query.answer('Верно ✅')

            await clean_messages(state, callback_query.message)

            message_to_delete = await _send_question(callback_query, session, question.test_id, state)

            async with state.proxy() as data:
                data['delete_messages'] = [message_to_delete.message_id]

            return

        await callback_query.answer('Не верно ❌')

        selected_answers = right_answers
        wrong_answers = data['selected_answers']

        is_answered = True

        async with state.proxy() as data:
            data['is_answered'] = is_answered

    else:
        async with state.proxy() as data:
            data['selected_answers'][index - 1] = match
            selected_answers = data['selected_answers']
            await callback_query.answer('Выбрано 👍')

    await callback_query.message.edit_reply_markup(
        reply_markup=get_question4x4_inline_markup(await get_question(session, data['question_id']),
                                                   data['chapter_id'], selected_answers=selected_answers,
                                                   wrong_answers=wrong_answers, is_answered=is_answered))


async def _send_question(callback_query: CallbackQuery, session, test_id, state):
    async with state.proxy() as data:
        if 'questions' not in data:
            data['questions'] = list()

    questions = await get_questions(session, test_id, exclude_ids=data['questions'])

    test = await get_test(session, test_id)

    if not questions:
        await state.finish()
        await callback_query.message.answer(
            f'Вопросы закончились 🤟\n\nТема: <i>{test.name}</i>\nНабрано <b>{data["user_balls"]}</b> '
            f'из <b>{data["total_balls"]}</b> возможных баллов\n' 
            f'Процент правильных ответов: <b>{round(data["user_balls"] * 100 / data["total_balls"])} %</b>')
        return await callback_query.message.answer('Выберите тему 👇',
                                                   reply_markup=await get_chapter_inline_markup(session))

    question = random.choice(questions)

    if question.test_type == '4x1':
        await Test.question_4x1.set()
        markup = get_question4x1_inline_markup(question, test.chapter_id)
    elif question.test_type == '4x4':
        await Test.question_4x4.set()
        markup = get_question4x4_inline_markup(question, test.chapter_id)
    else:
        raise Exception('No such question format')

    async with state.proxy() as data:
        data['question_id'] = question.id
        data['test_id'] = test.id
        data['chapter_id'] = test.chapter_id
        data['is_answered'] = False
        data['selected_answer'] = None
        data['selected_answers'] = [None, None, None, None]
        data['questions'].append(question.id)
        if 'total_balls' not in data:
            data['total_balls'] = 0

        if 'user_balls' not in data:
            data['user_balls'] = 0

        data['total_balls'] += 1 if question.test_type == '4x1' else 4

    questions_count = await count_questions(session, test.id)

    if question.question_image:
        return await callback_query.message.answer_photo(f'https://zno.osvita.ua{question.question_image}',
                                                         caption=f'<b>{len(data["questions"])}</b>/{questions_count}\n'
                                                                 + (question.question if question.question else ''),
                                                         reply_markup=markup)
    return await callback_query.message.answer(
        f'<b>{len(data["questions"])}</b>/{questions_count}\n' + (question.question if question.question else ''),
        reply_markup=markup)
